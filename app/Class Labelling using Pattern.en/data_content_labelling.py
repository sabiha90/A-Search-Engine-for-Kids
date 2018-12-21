import csv
from pattern.en import sentiment, positive


"""
Method that calculates the document sentiment score for each sentence
"""
def get_document_sentiment(doc_content):
   score = 0.0
   n = 0
   positive_lines = 0
   negative_lines = 0
   for line in doc_content.split(". "):
       sentiment_score,_ = sentiment(line)
       n = n + 1
       if (sentiment_score >= 0.1):
           positive_lines = positive_lines + 1
       elif (sentiment_score < 0):
           negative_lines = negative_lines + 1

       score = ((score * n) + sentiment_score)/n
   score = score + (positive_lines/n) + (negative_lines/n)
   return score


"""
Method that writes the output of data content labelling to an output CSV file
"""
def write_to_file(writer, content):
   writer.write(content+"\n")


"""
Method that is invoked that parses all the documents from the input file final_data.csv. The sentences in each document 
are split and scores for each of the sentences are calculated separately. The score for a document is finally
the average scores for all the lines in the document.
"""
def classify_document():
   strongly_positive = []
   neutral = []
   weakly_positive = []
   strongly_negative = []
   weakly_negative = []
   with open('final_data.csv') as csv_file, \
       open("str_positive.csv", "w+") as str_positive, \
       open("str_negative.csv", "w+") as str_negative, \
       open("file_data_output.csv", "w+") as output_file:
       tag_document_mapping = dict()
       tag_set = set()
       csv_reader = csv.reader(csv_file, delimiter=',')
       line_count = 0
       write_to_file(output_file, "ID,TagSet,URL,TagClass,Score,Classifier,Text")
       for row in csv_reader:
           doc_number = row[0]
           doc_content = row[1]
           doc_tags = row[2]
           for tag in doc_tags.split(","):
               clipped_tag = tag.replace("'", "").replace("{", "").replace("}", "").strip().lower()
               tag_set.add(clipped_tag)
           doc_score = 0
           doc_score = doc_score + get_document_sentiment(doc_content)
           doc_classifier = ""
           if doc_score > 0.5:
               strongly_positive.append(doc_number)
               write_to_file(str_positive, doc_number + "," + row[3] + ",[" + "..".join(tag_set) + "]")
               doc_classifier = "strongly_positive"
           if doc_score > 0 and doc_score < 0.5:
               weakly_positive.append(doc_number)
               doc_classifier = "weakly_positive"
           if (doc_score < -0.3):
               strongly_negative.append(doc_number)
               write_to_file(str_negative, doc_number + "," + row[3] + ",[" + "..".join(tag_set) + "]")
               doc_classifier = "strongly_negative"
           if (doc_score> -0.3 and doc_score < 0):
               weakly_negative.append(doc_number)
               doc_classifier = "weakly_negative"
           if doc_classifier != "":
               output_data = [doc_number,str(doc_tags), row[3], row[4], str(doc_score), doc_classifier, doc_content]
               write_to_file(output_file, ",".join(output_data))
       print(strongly_positive)
       print(strongly_negative)
       print(weakly_positive)
       print(weakly_negative)


"""
Method that is initiated first that invokes the method for classification
"""
if __name__ == '__main__':
   classify_document()



