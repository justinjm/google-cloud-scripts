library(here)

infile <- here("bq_migration", "loan_200k.csv")
outfile <- here("bq_migration", "loan_200.csv")

data_raw <- read.csv(file = infile)

data_out <- data[,!names(data_raw) %in% c("default")]

names(data_out)

write.csv(data_out,
          file = outfile,
          row.names = FALSE)