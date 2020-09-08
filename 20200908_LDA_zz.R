## Process text
library(tm)
library(SnowballC)
# Concert the abstract in metadata to the corpus format in tm 
abs <- Corpus(VectorSource(md01$abstract))
# Remove spaces
abs <- tm_map(abs, stripWhitespace)
# Convert to lower case
abs <- tm_map(abs, content_transformer(tolower)) 
# Remove pre-defined stop words ('the', 'a', etc)
abs <- tm_map(abs, removeWords, stopwords('english'))
# Convert words to stems ("education" = "edu") for analysis, for more info see  http://tartarus.org/~martin/PorterStemmer/
abs <- tm_map(abs, stemDocument)
# Remove numbers
abs <- tm_map(abs, removeNumbers, lazy=TRUE)
# remove punctuation
abs <- tm_map(abs, removePunctuation, lazy=TRUE)

## LDA Topic Modelling

# Term Frequency Inverse Document Frequency
dtm.tfi <- DocumentTermMatrix(abs, control = list(weighting = weightTf))
# Remove zero entries
rowTotals <- apply(dtm.tfi , 1, sum) #Find the sum of words in each Document
dtm.tfi   <- dtm.tfi[rowTotals> 0, ]

# Find appropriate k for the LDA Model
library(topicmodels)
PERPvector <- vector(length = 49)
for (i in 2:50) {
  abs.lda = LDA(dtm.tfi, k = i)
  PERPvector[i] <- perplexity(abs.lda)
}
plot(PERPvector, type="l", main = "Perplexity Plot", xlab="# of Topics Minus 1", ylab="Perplexity")
# The plot suggests that the number of topics may be larger than 50.

# Let the number of topics be 8 as the qualitative analysis suggests.
abs.lda = LDA(dtm.tfi, k = 8)
# Word-topic probabilities
library(tidytext)
library(reshape2)
abs.topics <- tidy(abs.lda, matrix = "beta")
# Plot work-topic probabilities
library(ggplot2)
library(dplyr)
abs.top.terms <- abs.topics %>%
  group_by(topic) %>%
  top_n(10, beta) %>%
  ungroup() %>%
  arrange(topic, -beta)
abs.top.terms %>%
  mutate(term=reorder_within(term, beta, topic)) %>%
  ggplot(aes(term, beta, fill=factor(topic))) + 
  geom_col(show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free") +
  coord_flip() +
  scale_x_reordered()
