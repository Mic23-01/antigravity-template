import argparse, sys
import chromadb

REQUIRED = {
  "fix_logs": ["project","type","date","files","tests","result"],
  "research_summaries": ["project","type","date","topic","tags","sources"],
  "decisions": ["project","type","date","decision_id","status","topic","tags"]
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--collection", required=True)
    ap.add_argument("--id", required=True)
    ap.add_argument("--data-dir", default="/home/ubuntu/chroma-data")
    args = ap.parse_args()

    try:
        client = chromadb.PersistentClient(path=args.data_dir)
        col = client.get_collection(args.collection)
        got = col.get(ids=[args.id], include=["metadatas"])
        
        if not got["ids"]:
            print(f"FAIL: ID '{args.id}' not found in collection '{args.collection}'")
            sys.exit(1)
            
        md = got["metadatas"][0] if got["metadatas"] else None

        if md is None:
            print("FAIL: metadata is null")
            sys.exit(1)

        missing = [k for k in REQUIRED.get(args.collection, []) if k not in md]
        if missing:
            print(f"FAIL: missing keys: {missing}")
            sys.exit(1)

        print("PASS: metadata present and complete")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
