# Load the package required to read JSON files
library("rjson")

# Read all files in the data folder
path <- "../new data/JAIED_20132020/iaied_journal_json_1320"
filenames <- dir(path)
filepaths <- sapply(filenames, function(x) {paste(path, x, sep='/')})

data <- rjson::fromJSON(file = filepaths[1])
data <- data[-c(which(names(data)=="author"), which(names(data)=="keywords"))]
summary <- as.data.frame(data)

# Convert JSON file to CSV file
for (i in 2:length(filepaths)) {
  # Give the input file name to the function
  data <- rjson::fromJSON(file = filepaths[i])
  # Remove authors and keywords
    data <- data[-c(which(names(data)=="author"), which(names(data)=="keywords"))]
  # Convert JSON file to a data frame
  json_data_frame <- as.data.frame(data)
  # Add data frame to summary
  summary <- rbind(summary, json_data_frame)

  print(i)
}

# Store data frame to CSV
write.csv(summary, '../new data/JAIED_20132020/test.csv', row.names=FALSE)
