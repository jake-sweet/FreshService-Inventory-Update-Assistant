I wrote this as an intern for the company I worked for at the time. It pulls data from SentinelOne to update the ticketing system's asset inventory (FreshService), specifically for laptops. It is my first ever real program (as in, written in the real world and not as a school assignment), so it's not the prettiest and doesn't follow any kind of specific etiquette or standard, but it got the job done and it got it done well. The idea was to create a .csv file to import to FreshService by gathering serial numbers from SentinelOne and then looping those through the Lenovo warranty API to get model names for the associated laptops, then looping back through the SentinelOne API to gather all remaining data for each machine associated with a serial number.

Unfortunately, this program only works with valid API keys and tokens, which are only available in an enterprise environment, so, given that I am no longer working at that company, this program can no longer be used by me. However, if you happen to have the same exact, unique problem that prompted me to write this script in the first place, feel free to use it. Like I said, it works well. 

Included in this repository will be the README.txt that I wrote for my co-workers to provide the most thorough documentation I could for use and update of the program. I am not a professional developer or technical writer, so please apologize the hasty messiness of my code and associated documentation.

I have replaced all potentially confidential information in the README.txt and within the script itself with "****".

I apologize again for a lack of etiquette and cleanliness, not just within the code and documentation itself, but within this upload/repository. This is the first time I have ever uploaded to GitHub.

With all of that said, thank you for stopping by, and I hope that, whoever you are, you are well-loved and well-hydrated. You deserve it!

Requirements

 - Must have a Python interpreter - will be covered momentarily - you want the most recent version of Python, and make sure to check what kind of processor you have to make sure you get the right version in that regard
 - Must have a decent internet connection
 - Must have Excel
 - Must have a valid SentinelOne API key - generate one by logging into SentinelOne, clicking your user profile in the top right, selecting "My User", clicking "Actions" -> "API Token Operations" -> "Generate/Regenerate API Token" and copying the key that pops up. These tokens expire monthly so if the program fails, one likely cause is the S1 API token having expired. Once you have a token, store it safely in the same **** folder you found this program in by editing the **** text file and following the established syntax (deleting any expired tokens and updating with correct date range)

Python

 - Navigate to https://www.python.org/downloads/release/python-3124/ and download the appropriate version (likely the recommended x64)
 - Once the download is complete, launch the executable. Select "install as administrator" and then "custom installation"
 - Select everything but the debug options and continue through the rest of the prompts until it's complete
open cmd as administrator and issue the command "python --version" to check your installation went properly; follow this up with "pip install x", replacing "x" with all the modules imported at the start of the program (json, requests, csv, and re)

Tutorial

 - First, navigate to the **** and locate ****. Copy and paste the Inventory Update Assistant folder into your Temp folder (C:/Windows/Temp)
 - Enter the pasted folder and open the **** file to copy your API token (if it hasn't expired), run inventory_update_assistant.bat, and paste the token upon being prompted
 - For more interactive use or for debugging, just open the file in a text editor and copy/paste functions into your Python interpreter as described above (will have to copy up to sentinelonekey and then input the key before copying and pasting the rest)
 - Once the script has finished running you should see a new file in your Inventory Update Assistant folder titled Assets CSV.csv. Feel free to open this for review
 - Once you have this CSV file, go to FreshService -> Assets -> Inventory, and select "Import" from the top right. Follow the prompts, select Laptops for type, leave Match Records By on Serial Number, and the rest should be intuitive. Note: this CSV file will not overwrite existing data, it simply adds to the inventory. This means that if a machine is assigned to a user who no longer uses it, you will still have to manually remove that asset from that user at some point

Imports & Global Variables

 - Importing json for formatting, requests for API calls, csv for writing out to a CSV file at the end, and re for searching strings
sentinelonekey and lenovokey are both confidential tokens/keys necessary for accessing Apex's API URI's - keep these secure
 - The variables pattern I'm about to describe are repeated later so I will describe them in more generic terms. URL is the URI just mentioned and includes embedded filters you can see after the "?" (in url_sentinelone's case, the filters allow a limit of 1000 returns, it skips counting the returns, and only searches for laptops). The headers variable formats the API auths, r_ is the actual API request and it passes the url and the headers through. List is specific to sentinelone since the API return comes in the form of a list of a dictionaries within a broader dictionary. Technically, sentinelone_list is a dictionary and sentinelone_dictionary is a list of dictionaries. Basically what these two variables do is get you inside the important list of dictionaries, so that the list can be iterated through in a loop for each and every dictionary later on. It easiest to think, when working with sentinelone_dictionary, since you will always be iterating through it, that you will always be working with a dictionary. In other words, as long as sentinelone_dictionary always exists in the context of a loop like "for x in sentinelone_dictionary". you are indeed working with a dictionary. Confusing, I know, but this should be the takeaway: sentinelone_list isn't really that important, and sentinelone_dictionary can be thought of as a dictionary for the purposes of the script
serial and models are both just a list and a dictionary respectively that I pre-defined so that they could be updated and appended to later on in various functions
 - There are three variables that are defined/redefined later on in the program: serial, models, and tapestry. All three are just defined as the return of their associate functions

API credentials

 - API credentials can be found securely stored in the script itself or in the **** under ****

sentinelone()

 - This function's purpose to produce a list of our laptops' serial numbers for later use
 - On a technical level: for every dictionary in sentinelone_dictionary, for those key/value pairs where the key is "serialNumber", the value is appended to the list serial
 - In other words: this function finds serial numbers in every dictionary sentinelone gives us and puts them in a list

lenovo()

 - This function's purpose is to create a dictionary where the serial numbers from the previous function are the keys, and their corresponding model names are the values, as well as establish a list of dictionaries (one for each serial number) for use in a later function
 - Variables should be relatively self-explanatory as they follow the pattern previously established. The reason they are defined within the variable and not globally is because, unfortunately, of the way the function must work (it makes a single API call for every serial number, meaning the url has to be an f string in order to embed the serial numbers for every iteration, meaning it has to be defined within the for loop)
 - On a technical level: the function first iterates through the previously developed serial list, passing through each serial number into individual API calls to Lenovo's warranty API. Once we have an API call, we iterate through the key/value pairs of the dictionary returned and where the key is "Product", we begin an if/else statement that extracts the desired info from the string in the value slot and then updates it to the globally defined dictionary models with the serial number being the key and the model name being the value. The else statement mostly exists because of how anomalous the Legions are within the Apex inventory
 - In other words: this function runs through one Lenovo warrant API call at a time and grabs the model name associated with the embedded serial number and then adds these to a dictionary. The goal of doing this is to create a legend which tells us what model each machine is

weave()

 - This function's purpose is to create a list of dictionaries which each have the same keys but which have different values; in this case, we want the username, asset tag, model name, serial number, and operating system of every laptop in the form of a series of dictionaries
 - Variables are all lists and should be self-explanatory until tracker, semi, and total. Those three variables serve are used in a for loop at the end of the function designed to remove duplicate entries created by the function's penultimate loop. This is not ideal, but given this was a quick project and doesn't require much computing power to begin with, this is okay for now. If anyone can find a way to re-factor the function such that duplicates are not created in the first place, that would be ideal
 - On a technical level: we start with a for loop yet again iterating through our list of serial numbers - this ensures that no matter what, we will not encounter any list index errors and the program should always run. The next for loop iterates through sentinelone_dictionary, and then checks to make sure that the dictionary x represents has all the specified keys in it before proceeding. Next, we iterate through the retrieved dictionary's keys and when we find a value that equals the serial number we are on, we first append the serial number to the list number, and then iterate through the models dictionary to find the matching serial number and append the associated value from the models dictionary to the list product. Next, knowing we are still on the same serial number, we re-iterate through the x dictionary (from sentinelone_dictionary) to find the keys "lastLoggedInUserName", "computerName", and "osName" and append their corresponding values to lists user, asset, and os respectively. Next are a series of print statements to check that each list is the same length, followed by the cherry on top, a for lop that runs through each list and defines a temporary dictionary with the keys "Used By", "Asset Tag", "Product", "Serial Number", and "Operating System", injecting the corresponding element from each list as the values for each of these keys (user for "Used By", etc.). Because each list was created using the same exact serial numbers as reference points, this will work since they will be ordered accordingly. Note: FreshService does not accept plaintext usernames, so "Used By" and "User" are two different things, the former being an email address, and the latter being plain usernames. Lastly, the aforementioned duplicate elimination loop, which takes given dictionary from the list of dictionaries semi and tries to find it again within the same list, eliminating duplicates if it finds any
 - In other words: this function takes a serial number from the list created earlier and then runs through the SentinelOne API to find that serial number and appends all of the other corresponding data from the discovered dictionary to separate lists. Once these lists are created, they are "woven" together into a list of dictionaries, such that each dictionary represents a single machine, the keys are the "columns", and the values are the data returned in the previous for loop. The reason the x dictionary's key/value pairs are iterated in the nested way that you see is so that when we go to actually find the data we want, we are sure that we have a corresponding serial number.

excel()

 - This function is very simple - all it does is take tapestry (the list of dictionaries built from weave()) and write it out to a CSV file for importing the FreshService. It is designed the way that it is to meet FreshService's formatting standards for the import process
 - On a technical level: first, the column names are defined as field_names. Then a save location is specified and a new CSV file is opened for writing. After that, the CSV file is written, passing through field_names as the field names (surprise!) and the rows are taken from tapestry
 - In other words: excel writes tapestry to a CSV file

search()

 - This function is also very simple - all it does is allow the user to search for specific entries in tapestry by name, asset tag, model name, serial number, or operating system (worth noting this function is case-sensitive and requires full strings - call me lazy but I just made these for troubleshooting and review purposes)
 - On a technical level: first an input variable, search, is defined, which asks the user what they would like to search for. Then five different search loops are defined, each working the same way. Starting with an if statement, the script determines what you are searching by. Then another input variable is defined, asking the user what the username or asset tag, etc. they are searching for is. Then a for loop iterates through every dictionary within tapestry and then runs through the key/value pairs found within said dictionary to find the string provided for the input variable. If a value is found that matches the string input, the whole dictionary is printed
 - In other words: this function allows you to search through the tapestry list of dictionaries for machines based on any of values in the dictionary (username, asset tag, etc.)

Troubleshooting

The lenovo() function is the most annoying and likely most problematic function in the script. The reason for this is the if/else statements and the way they search for model names. If you begin to see gaps in the output of weave()/tapestry that you wouldn't expect, or the program begins outputting list index errors around weave(), the best way to troubleshoot the issue would be by using the debug function.

The reason the debug() function wasn't explained earlier is because it will be explained here. The function debug() will create a list containing the serial numbers of machines that did not get caught in weave(). At this point the user can plug these serial numbers into Postman to analyze the lenovo warranty API for anomalies.

In all likelihood, you will find some quirk to the raw model name string that is unfortunately unable to be accounted for until it is discovered. in this case, you need to pipe that anomalous substring into the re.search() line within weave() in a way that will allow the machines to be caught by the function. For a real example, there were some models (T490's in this case) that had different characters surrounding their model name than the other T490's, so I piped that different character into the (?=) portion of that line. If you find another issue like this, do the same. For a hypothetical example, imagine you find a T490 that is followed by a character not included in this line, a "+" symbol in this case. What you would do is take the character and pipe it into the parenthetical, changing it from (hypothetically) (?=-TYPE) to (?=-TYPE|+). This will allow the search method to include this newfound anomaly in the search. 

Permission to create .csv denied? Try deleting the old one in your Temp folder before running the script again.