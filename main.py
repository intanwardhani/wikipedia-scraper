# UTF-8 Python 3.13.5
# A driver script that import classes and sets up the workflow structure
# Author: Intan K. Wardhani

import time
import logging
from wikiscrapers.leaders import Leader
from wikiscrapers.paragraphs import Paragraph
from wikiscrapers.filemanager import Save

def main():
    
    """Main workflow for extracting leaders, parsing their Wikipedia pages, and saving the results."""

    logging.basicConfig(
        filename="leaders_workflow.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8"
    )

    start_time = time.perf_counter()
    print("=== Starting Leader Extraction Workflow ===")
    logging.info("=== Starting Leader Extraction Workflow ===")

    session = None  # <-- initialise to avoid unbound warning

    try:
        # Step 1: Initialise Leader (creates session)
        leader_api = Leader()
        session = leader_api.session  # reuse this session everywhere

        # Step 2: Initialise other classes with the same session
        paragraph_extractor = Paragraph(session=session)
        storage = Save()

        # Step 3: Fetch leaders and Wikipedia pages
        print("Fetching leaders and Wikipedia pages...")
        leaders_per_country, wiki_responses = leader_api.get_leaders()
        
        print(f"Fetched leaders for {len(leaders_per_country)} countries.")
        logging.info(f"Fetched leaders for {len(leaders_per_country)} countries.")

        # Step 4: Extract and clean first paragraphs
        print("Extracting first paragraphs from Wikipedia pages...")
        paragraphs_per_leader = []

        for resp in wiki_responses:
            lang, paragraph = paragraph_extractor.get_first_paragraph(resp)
            if paragraph:
                paragraphs_per_leader.append({
                    "url": getattr(resp, "url", "unknown"),
                    "language": lang,
                    "paragraph": paragraph
                })

        print(f"Extracted {len(paragraphs_per_leader)} clean paragraphs.")
        logging.info(f"Extracted {len(paragraphs_per_leader)} clean paragraphs.")

        # Step 5: Save results to JSON
        print("Saving data to leaders.json...")
        storage.export_json("leaders", {
            "leaders_per_country": leaders_per_country,
            "paragraphs_per_leader": paragraphs_per_leader
        })

        print("Workflow complete. Data saved to 'leaders.json'.")
        logging.info("Workflow complete. Data saved to 'leaders.json'.")

    except Exception as e:
        logging.error(f"Workflow failed: {e}", exc_info=True)
        print(f"Workflow failed: {e}")

    finally:
        if session is not None:
            session.close()  # safe to close only if created
        elapsed = time.perf_counter() - start_time
        logging.info(f"Workflow finished in {elapsed:.2f} seconds.")
        print(f"Workflow finished in {elapsed:.2f} seconds.")

if __name__ == "__main__":
    main()


