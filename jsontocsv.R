# Load the package required to read JSON files
library("rjson")

# Read all files in the data folder
path <- "../data/iaied"
filenames <- dir(path)
filepaths <- sapply(filenames, function(x) {paste(path, x, sep='/')})

# Convert JSON file to CSV file
for (i in 1:length(filepaths)) {
  # Give the input file name to the function
  data <- rjson::fromJSON(file = filepaths[i])
  # Remove authors and keywords
    data <- data[-c(which(names(data)=="author"), which(names(data)=="keywords"), which(names(data)=="abstract"))]
  # Convert JSON file to a data frame
  json_data_frame <- as.data.frame(data)
  # Store data frame to CSV
  write.csv(json_data_frame, paste('../data/iaied_csv/', sub(".json", ".csv", filenames[i]), sep = ""), row.names=FALSE)
  print(i)
}
