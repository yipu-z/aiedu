# aiedu

## 10/30/2020 - Jie Chen
[New] `regulate_data.py` - Change some author names who use different names in file.  
[New] `text_process.py` - Process full paper text.  
[Update] Create `code_keywordanalysis` and `code_datacollection` folders and arrange code files.  

## 09/22/2020 - Jie Chen
[New] `extract_htmlinfo_tojson.py` - Have conference html files, extract useful info, get json files.  
[New] `miner_aied_journal_web.py` - Extract paper links from official website, then get journal html files, extract useful info, get json files.  


## 08/25/2020 - Jie Chen
[New] `commonkeywords_fromkws.py` - Get common keywords from keyword corpus. Result is in `keyword_dict.csv`.  
[New] `ngram_model.py` - (1) Get n-gram model from abstract text; (2) Find context of negative words in abstracts. Trigrams are in `neg_trigrams.txt`.  
[Update] `sentimentanalysis.Rmd` - Get negative words by both nrc and bing lexicons. Negative words from both lexicons have been merged in `neg_wordlist.csv`.  

## 08/22/2020 - Jie Chen

[New] `socialnetworkanalysis.Rmd` - Pilot view of social network analysis.  
[New] `sna_matrixprocessing.py` - The output is a sna table (`sna_table.csv`) which is about authors' relations. The SNA graph is also generated by networkx.  
[New] `authorinfo_toecharts_pre.Rmd` & `authorinfo_toecharts.py` - Discover the visualization by Echarts. The mediate output is `author_table_echarts.json` and `relation_echarts.json`. The final output of these two files is `echarts.json`, which can be used in Echarts.  
[New] `mergejson_summary.py` - Merge all paper info json files into one `json_summary.json` file.  
[Updated] `sentimentanalysis.Rmd` - Sentiment analysis of abstracts.  
[Updated] `jsontocsv.R` & `jsontocsv_summary.R` - Convert JSON file, which contains paper info, to CSV file. The output of jsontocsv.R is a folder with separate csv files. The output of jsontocsv_summary.R is a `summary.csv` containing all information in one csv file.   
[Updated] `springerminer.py` & `run.py` - Extract author, abstract, RIS, and more paper information from Springer  
[Updated] `paperminer.py` - Extract abstracts from IAIED  

## 03/08/2021 - Jie Chen
### Data Collection
`extract_htmlinfo_tojson.py` - Extract journal and conference data from Springer in json format  
`get_paper_links.py` - Get Springer conference/journal links   
`miner_lak_journal_web.py` - Get LAK journal citations, web version.  
`springerminer_api.py` - Get Springer metadata by using API.   
`tandf_requests.py` - Use requests to get Journal of Learning Sciences reference download links.   
### Keyword Analysis
`keyword_process.py` - Process json data for getting keywords, then process keywords and generate NLP table, keyword frequency table and common keyword table.   
`keyword_process_copyforbib.py` - Process bib data, and generate same tables as above.   
`lak_title_keyword.py` - Same as above but generate one more article title and keyword table.   
### Other Analysis
`find_affiliation.py` - Extract authors' affiliations by educational institutions and non-educational institutions. The output is two json files by ed and non-ed.   
`recommender.py` - Recommend papers by abstracts using tfidf and consine similarities.   
`ngram_model.py` - Get n-gram from abstract and see frequency.   
`regulate_data.py` - Get all author names and regulate name data through observation and checking their last name.   
`sna_1002.py` - Get unique author names and then generate the relationship graphs.   
`text_process.py` - many useful functions for finding adhesive words or sentence   
 
