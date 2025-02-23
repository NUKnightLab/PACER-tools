# Table of Contents
* [Scraper Tutorial](README.md#scraper-tutorial)
    1) [Getting Started](README.md#1-getting-started)
    2) [Pacer credentials](README.md#2-pacer-credentials)
    3) [Query Scraper](README.md#3-query-scraper)
    4) [Docket Scraper](README.md#4-docket-scraper)
    5) [Document Scraper](README.md#5-document-scraper)
* [Parser Tutorial](README.md#parser-tutorial)

# Scraper Tutorial
This is a tutorial on how to use the SCALES Scraper tool to download data from PACER. 

The scraper has three modules:

 1. Query scraper: to download case queries
 2. Docket Scraper: to download case dockets
 3. Document Scraper: to download case documents

This tutorial will step through the basics of getting set up with the scraping tool and using each module. For more details, see the documentation [here](code/downloader/README.md)

The tutorial uses the PACER demo site located here: https://dcecf.psc.uscourts.gov/cgi-bin/ShowIndex.pl

This is a demo version of PACER with demo credentials that can be used for free. It contains a sample of cases from Western District of New York (*nywd*). However because it runs on its own domain with *psc* (PACER Service Center) instead of on the *nywd* PACER site, we will use **psc** as the court abbreviation for this tutorial.

## 1. Getting Started

 - Clone this PACER-tools repo
 - Install any missing python packages (see below)
 - Make sure you have a recent version of Firefox installed (80.0+) and [GeckoDriver](https://github.com/mozilla/geckodriver) for Firefox

### Installing packages

This project was originally developed for use with the [Anaconda](https://www.anaconda.com) python distribution. 

Anaconda users can create a new project using `conda install -n PACER-tools requirements.txt`; change *PACER-tools* to any other project name if you prefer.

If you are not an Anaconda user, you can install the python requirements for this project using `pip install -r pip-requirements.txt`; we recommend creating a separate virtual environment for this project.  The reference Python used for development is `3.8.5` but this should work with any `3.8.x` and probably with any version of Python 3.

Anaconda also manages installation of many non-python dependencies. Non-Anaconda users may have to install these themselves, in ways which may vary from platform to platform. A list of the non-python dependencies is included, in a series of commented lines, at the end of `pip-requirements.txt` but they may not all be needed, and installing them will vary. If you use PACER-tools without using Anaconda, we welcome help improving the documentation about what needs to be installed, and, to the extent possible, how it should be installed.



### Download folder
For this tutorial we are going to put our data into *data/pacer*. The scraper separates out data by district, so it's best to have a subdirectory for each district, named by court abbreviation (e.g. *data/pacer/ilnd* for Northern District of Illinois). When the scraper runs it will build the necessary structure inside of that subdirectory that it needs to download and house the data from Pacer.

Since we are using the PACER demo, we will use the court abbreviation it uses which is *psc* (for PACER Service Centre). The scraper will take an `inpath` argument, to which we will pass */data/pacer/psc*.

## 2. Pacer credentials
For most use you will need to put your Pacer login details into a json file. For this tutorial we'll be using the Pacer training site with the login details contained in */code/downloader/login/demo.auth*. When you are running the scraper using your own credentials you can use that file as a template.

## 3. Query Scraper
The first thing we'll do with the scraper is download some query results. There is a demo query located at */code/downloader/demo.json*. This is a *.json* file that maps search criteria to fields in the Pacer query form.
 To create your own query later you can use the query builder (see the documentation).

Throughout this tutorial we will be running the scrapers.py file from the */code/downloader* folder, and all paths are relative to this (but it can be run from anywhere, with relative paths adjusted accordingly).

**Running script**

To use the Query Scraper we just need to run the following:

    python scrapers.py --override-time --query-conf demo.json ../../data/pacer/psc

 - *The `--override-time` flag is to override time restriction (as it is designed to run be run overnight)
 - The `--query-conf` option points the scraper to a json config file with the parameters for our query.

The user will be prompted for the following:

 - **Mode**: for this step we want to choose *query*
 - **Court**: for the demo site the court abbreviation we want to enter is *psc*
 - **Auth path**: This is the relative path to our PACER login credentials. Running this from the *downloader* folder the path to the demo credentials is *login/demo.auth*
 - **Case limit**: This limits the number of cases downloaded in a single session, to prevent accidental overspending on PACER. For this example lets just enter 50.

*Note*:
*All of these parameters that the user was prompted for can actually be given as arguments to the script. These are all explained in full in the documentation. To avoid the prompting you can instead run:*

    python scrapers.py --override-time --query-conf demo.json -m query -c psc -a login/demo.auth -cl 50 ../../data/pacer/psc


**Result**
Once these values have all been input, the Scraper should launch at this point and download the query results. You should see in the terminal the following message:
  
> Query results saved to <path_to_psc>/psc/queries 

If you navigate to the *psc* folder you will see firstly that a few subfolders have been created to house the data, and secondly within the *queries* folder there should be a *.html* file that contains the query results.


## 4. Docket Scraper
Next we will take that query results file and download all of the dockets for the listed cases. The Docket Scraper module can take a *.html* query file, which we have just downloaded, as its input.

**Running script**
To use the Docket Scraper we will run the following:

    python scrapers.py -m docket --docket-input ../../data/pacer/psc/queries/<query_file>.html -c psc -a login/demo.auth -cl 50 --override-time ../../data/pacer/psc

 - The `--docket-input` option takes the path to the query file. The actual name of the query file (`<query_file>`) will vary as it includes a timestamp.

The Docket Scraper (as well as the Document Scraper which will look at next) runs asynchronously across multiple Firefox instances, by default two. The no. of instances (workers) running can be adjusted by the `n-workers` option (see the documentation).

*Note: the scraper only keeps the civil and criminal cases, to download a specific case type you can use the ``--case-type`` option.*

**Result**
Once both browsers have finished and closed, all of the cases from the query results file should be downloaded and can be found in */data/pacer/psc/html*



## 5. Document Scraper
Lastly, we will get the actual documents associated with docket lines of the cases. The docket scraper can take a few different types of inputs, including a list of specific cases, but for this tutorial we will give it the directory of docket *.html* files as an input so that documents for all cases will be downloaded. By default, for each case all documents and attachments will be downloaded.

**Running script**
To use the Document Scraper we run the following:

    python scrapers.py -m document -c psc -a login/demo.auth -cl 50 --override-time ../../data/pacer/psc
    

 - When no input is specified, the Document Scraper will include all dockets in the */html* directory in the download. To download documents for specific documents see below.
 - There is a default limit of 1000 documents per case. Any case that has more than 1000 documents will be skipped. This limit can be changed by the  `--document-limit` option.

**Result**
The Document Scraper will usually take significantly longer to run than the Docket Scraper given the volume of documents in most cases. Once the documents have finished downloading they can be found in the */data/pacer/psc/docs* folder.
 

 **Attachments and specific documents**
 

 - To skip docket line attachments you can use the `--no-document-att` flag.
 - To get specific documents from specific cases, you can use the `--document-input` option to pass a *.csv* file with cases ids and list specific documents to retrieve, see the documentation for more.


To see more specifics, options and use cases check out the detailed documentation [here](code/downloader/README.md).

# Parser Tutorial

This short section explains how to use the SCALES Parser tool to read HTMLs downloaded from Pacer and convert them into JSON format. The parser takes as its input the results of running the [docket scraper](README.md#4-docket-scraper) - namely, a folder of HTMLs.

**Running script**
To use the parser on the HTMLs from the docket scraper in the previous tutorial, we will simply run the following:

    python parse_pacer.py ../../data/pacer/psc/html ../../data/pacer/psc/json

**Result**
Once the parser has finished, all the parsed versions of the HTML files can be found in */data/pacer/psc/json*.

To see more specifics, options, and details on the JSON schema, check out the detailed documentation [here](code/parsers/README.md).
