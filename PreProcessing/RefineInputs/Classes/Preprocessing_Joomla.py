/*******************************************************************************
 * Copyright (c) University of Ottawa 2022-2024
 * Created by Nazanin Bayati (n.bayati@uottawa.ca)
 *     
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *  
 *  http://www.apache.org/licenses/LICENSE-2.0
 *  
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *******************************************************************************/


from nltk.stem import PorterStemmer, WordNetLemmatizer
from unicodedata import normalize
import pandas as pd
import json
import re
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import warnings
warnings.filterwarnings("ignore")

class preProc_joomla:

    def split_lines_by_marker(filename, marker="**********************************************"):
        with open(filename, 'r') as file:
            current_sublist = []
            for line in file:
                if marker in line:
                    if current_sublist:
                        yield current_sublist
                        current_sublist = []
                else:
                    current_sublist.append(line)
            if current_sublist:
                yield current_sublist


    def __init__(self, target_dir, input_json):
        print("Starting Pre-processing")
        print("It will take a while...")

        new_row = {"sequence": [], "url": [], "index": [], "user": [], "method": [],
                   "output": [], "parameter":[]}
        self.df = pd.DataFrame(new_row)
        for sublist in preProc_joomla.split_lines_by_marker(target_dir):
            # Each sublist contains lines between markers
            sequence=''
            url=''
            index=''
            username=''
            method=''
            output=''
            parameter=''
            for l in range (sublist.__len__()):
                if sublist[l].startswith("!!!!!!!! Sequences: "):
                    sequence = sublist[l].split("!!!!!!!! Sequences: ")[1]
                elif sublist[l].startswith("!!!!!!!! URL: "):
                    url = sublist[l].split("!!!!!!!! URL: ")[1]
                    if url.__contains__('log in with'):
                        parameter = url.split("log in with ")[1].split(')')[0]
                        parameter = parameter+')'
                elif sublist[l].startswith("!!!!!!!! index:"):
                    index = sublist[l].split("!!!!!!!! index:")[1]
                elif sublist[l].startswith("!!!!!!!! Username: "):
                    username = sublist[l].split("!!!!!!!! Username: ")[1]
                elif sublist[l].startswith("!!!!!!!! Method: "):
                    method = sublist[l].split("!!!!!!!! Method: ")[1]
                elif sublist[l].startswith("!!!!!!!!Print o1:"):
                    output = sublist[l+1]
            preProc_joomla.dataExtraction(self, sequence, url, index, username, method, output, parameter)
        # Get the index of the last row
        last_row_index = self.df.index[-1]

        # Remove the last row
        self.df = self.df.drop(last_row_index)
        preProc_joomla.id_matching(self, input_json)
        preProc_joomla.outputCleaner(self)
        preProc_joomla.writeToCsv(self, target_dir, input_json)
        unique_rows_count = self.df['output'].nunique()
        print(unique_rows_count)

    def outputCleaner(self):
        for i in range(self.df['output'].__len__()):
            output = self.df['output'].loc[i]
            self.df['output'].loc[i] = preProc_joomla.outputCleaning(self, output)


    def outputCleaning(self, output):
        # removing the stop words
        # removing special characters
        # removing common words like menues
        # Removing tags, footer, date and time
        if str(output) == 'nan':
            output = ''
        output = [re.sub(r"\([a-zA-Z]+ [0-9]+, [0-9]+ ([0-9]+:)+[0-9]+ [A-Z]+\)", ' ', k) for k in output.split("\n")][
            0]
        # output = [re.sub(r"([0-9]+(.[0-9]+)*) [yr|mo|day|hr|min|sec|ms]+", ' ', k) for k in output.split("\n")][0]
        # removing special characters and numbers and Menu, header and footer
        output = str(output)
        output = output.replace(u'\\xa0', '')
        output = output.replace(u'\xa0', '')
        output = output.replace(' ', '')
        output = normalize('NFKD', output)
        output = output.replace('â€˜', '')
        output = output.replace('Â»', '')
        output = re.sub(r'[^A-Za-z\s]', '', output)
        output = output.lower().replace('sut', '')
        output = output.lower().replace('home', '')
        output = output.lower().replace('news', '')
        output = output.lower().replace('sport', '')
        output = output.lower().replace('travel', '')
        output = output.lower().replace('culture', '')
        output = output.lower().replace('contact', '')
        output = output.lower().replace('back to top', '')
        output = output.lower().replace('popular tags', '')
        output = output.lower().replace('joomla', '')
        output = output.lower().replace('latest', '')
        output = output.lower().replace('articles', '')
        output = output.lower().replace('tag', '')
        output = output.lower().replace('tags', '')


        #removing stop words
        words_to_remove = ["publisher", "author", "editor", "admin", "wrong", "tag","enter","part","site","setting","settings"
            , "january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
                           "november", "december"
            , "checked", "the", "five", "most", "creative", "cities", "in", "world", "germanys", "germany", "tiny",
                           "geographic", 'search', "oddity", "transfer", "done", "deals", "window", "october",
                           "libra", "paypal", "first", "to", "drop", "out", "facebook", "cryptocurrency", "facebook's",
                           "could be misused", "says", "treasury", "chief", "mnuchin", "toggle", "navigation", "tag",
                           "deal",
                           "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "day",
                           "getting", "started", "menu", "profile",
                           "submit", "article", "login", "form", "hi", "module", "city", "close", "count", "counti",
                           "email", "address"]

        # output = output.lower().replace('city city', 'city')
        # Split the text into words
        words = output.split()
        # Create a new text with words not in the words_to_remove list
        output = " ".join(word for word in words if word.lower() not in words_to_remove)

        stop_words = set(stopwords.words('english'))
        output =output.lower()
        output = re.sub(r'\d+', '',output)
        word_tokens = word_tokenize(output)
        # converts the words in word_tokens to lower case and then checks whether
        # they are present in stop_words or not
        word_tokens = [re.sub(r'[^\w\s]', '', w) for w in word_tokens]
        # re.sub(r'\d+', '', text)

        word_tokens = ' '.join(word_tokens)

        word_tokens = word_tokenize(word_tokens)

        filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
        # with no lower case conversion
        filtered_sentence = ' '.join(filtered_sentence)
        output = filtered_sentence
        # string = output
        # Tokenize the string into words
        words = word_tokenize(output)

        # Initialize a PorterStemmer and a WordNetLemmatizer
        ps = PorterStemmer()
        wnl = WordNetLemmatizer()

        # Perform stemming and lemmatization on each word
        stemmed_words = [ps.stem(w) for w in words]
        lemmatized_words = [wnl.lemmatize(w) for w in words]

        output = ' '.join(lemmatized_words)


        number_pattern = r'\b(?:one|two|three|four|five|six|seven|eight|nine|ten)\b'

        # Use the re.sub function to replace matched patterns with an empty string
        output = re.sub(number_pattern, '', output, flags=re.IGNORECASE)
        output = output.lower().replace('counti', '')
        return output

    def dataExtraction(self, sequence, url, index, username, method, output, parameter):

        # sequence = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', sequence)
        sequence = re.findall(r'http[s]?://[^\s\],]+', sequence)

        if username.__contains__("admin"):
            username = 'admin'
        elif username.__contains__('publisher1'):
            username = 'publisher1'
        elif username.__contains__('editor1'):
            username = 'editor1'
        elif username.__contains__('author1'):
            username = 'author1'
        elif username.__contains__('wrong'):
            username = 'wrong'
        elif username.__contains__('null'):
            username = ''
        elif username.__contains__('username= '):
            username = ''

        if url.__contains__(']'):
            url = url.split(']')[0]
        if url.__contains__('http'):
            url = url.split(' ')
            url = url[url.__len__()-1]

        index = index.split('\n')[0]
        method = method.split('\n')[0]
        # output = preProc_joomla.outputCleaning(self,output)
        # Append data to the DataFrame
        new_row = {"id":'0',"sequence": sequence, "url": url, "index": index, "user": username, "method":method, "output": output, "parameter":parameter}
        self.df = self.df._append(new_row, ignore_index=True)

    def id_matching(self, input_json):

        with open(input_json, 'r') as json_file:
            data_json = json.load(json_file)
        for key, data in data_json.items():

            # Extract and concatenate the "url" values from the list of dictionaries
            # url_list = [entry_data.get('url', '') for entry_data in data]  # Use .get() to handle missing 'url' keys
            url_list = [entry_data.get('url', entry_data.get('elementURL', '')) for entry_data in data]

            combined_urls = ' '.join(url_list)
            # Split the combined URLs into a list of individual URLs
            url_list = re.findall(r'http[s]?://[^\s]+', combined_urls)

            # Check if any element in 'your_array' matches any cell in the 'sequence' column
            for i in range(self.df['sequence'].__len__()):
                a = self.df['sequence'].loc[i]
                b = self.df['id'].loc[i]
                if self.df['sequence'].loc[i] == url_list:
                    if self.df['id'].loc[i]=='0':
                        self.df['id'].loc[i] = key.split('path')[1]
                    elif key =='path8':
                        if i == 47:
                            self.df['id'].loc[i]='8'
                            self.df['id'].loc[i+1]='8'
                            self.df['id'].loc[i+2]='8'
                            self.df['id'].loc[i+3]='8'
                            self.df['id'].loc[i+4]='8'
                            self.df['id'].loc[i+5]='8'
                    elif key == 'path29':
                        if i == 145:
                            self.df['id'].loc[i] = '29'
                            self.df['id'].loc[i + 1] = '29'
                            self.df['id'].loc[i + 2] = '29'
                            self.df['id'].loc[i + 3] = '29'
                            self.df['id'].loc[i + 4] = '29'
                    elif key == 'path56':
                        if i == 253:
                            self.df['id'].loc[i] = '56'
                            self.df['id'].loc[i + 1] = '56'
                            self.df['id'].loc[i + 2] = '56'
                    elif key == 'path66':
                        if i == 307:
                            self.df['id'].loc[i] = '66'
                            self.df['id'].loc[i + 1] = '66'
                            self.df['id'].loc[i + 2] = '66'
                            self.df['id'].loc[i + 3] = '66'
                    elif key =='path78':
                        if i == 355:
                            self.df['id'].loc[i] = '78'
                            self.df['id'].loc[i + 1] = '78'
                            self.df['id'].loc[i + 2] = '78'
                    elif key == 'path88':
                        if i  in range(429,446):
                            self.df['id'].loc[i] = '88'
                    elif key == 'path89':
                        if i  in range(446,462):
                            self.df['id'].loc[i] = '89'
                            # self.df['id'].loc[i + 1] = '78'
                    elif key == 'path93':
                        if i in range(496, 508):
                            self.df['id'].loc[i] = '93'
                    elif key == 'path94':
                        if i in range(508, 520):
                            self.df['id'].loc[i] = '94'
                    elif key == 'path95':
                        if i in range(520, 532):
                            self.df['id'].loc[i] = '95'
                    elif key == 'path96':
                        if i in range(532, 544):
                            self.df['id'].loc[i] = '96'
                    elif key == 'path102':
                        if i in range(610, 624):
                            self.df['id'].loc[i] = '102'
                    elif key == 'path114':
                        if i in range(741, 744):
                            self.df['id'].loc[i] = '114'
                    elif key == 'path120':
                        if i in range(786, 789):
                            self.df['id'].loc[i] = '120'
                    elif key == 'path125':
                        if i in range(825, 835):
                            self.df['id'].loc[i] = '125'
                    elif key == 'path138':
                        if i in range(963, 966):
                            self.df['id'].loc[i] = '138'
                    elif key == 'path139':
                        if i in range(966, 971):
                            self.df['id'].loc[i] = '139'

                    elif key == 'path142':
                        if i in range(988, 991):
                            self.df['id'].loc[i] = '142'




                        # self.df['id'].loc[i] = key.split('path')[1]


                # self.df.loc[mask, 'id'] = replacement_number
            # print('')

    def writeToCsv(self, target_dir, input_json):
        df = self.df
        file_path = input_json.rsplit(".", 1)[0] + "_preprocessed.csv"
        # Split the file path into directory and file components
        directory, filename = os.path.split(file_path)

        refData_dir_parent = os.path.dirname(target_dir)
        path_to_output = os.path.join(refData_dir_parent, filename)
        df.to_csv(path_to_output, sep='\t', encoding='utf-8', header='true')

   
        refData_dir_parent = os.path.dirname(target_dir)
        path_to_output = os.path.join(refData_dir_parent, "outputs_preprocessed.csv")
        df.to_csv(path_to_output, sep='\t', encoding='utf-8', header='true')




