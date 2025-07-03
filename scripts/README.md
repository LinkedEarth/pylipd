# Step 1: Download compilations
python download_compilations.py --output-dir lipd_raw

# Step 2: Preprocess/update statistics  
python preprocess_compilations.py --input-dir lipd_raw --output-dir lipd_updated

# Step 3: Convert to GraphDB format
python convert_for_graphdb.py --input-dir lipd_updated --output-dir graphdb_ready

# Step 4: Upload to GraphDB
python upload_to_graphdb.py --ontology-dir ../ontology --endpoint http://localhost:7200/repositories/LiPDVerse-dynamic --username admin --password root --nq-zip-file graphdb_ready/all-lipd.nq.zip

# Step 5: (Optional) Analyse datasets compilation
python ./analyze_compilations.py --input-dir ./lipd_raw --output-dir ./lipd_analysis
