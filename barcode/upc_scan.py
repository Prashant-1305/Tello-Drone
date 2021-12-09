#Paxkage_Id__c
'''
	0064C00000CbEbMQAV		Drone A
3	0064C00000CbEbWQAV		Drone B
4	0064C00000CbFwOQAV	    Drone C
'''

import requests
import sys
sys.path.append('./python-zxing/')
import zxing

###### Constants ######
UPC_DIR = "./python-zxing/zxing/test_images"

UPC_TO_OPPORTUNITY_MAP = {"WAYFAIR_1": "0064C00000CbEbMQAV", "WAYFAIR_2": "0064C00000CbEbWQAV"}

RETRY_COUNT = 1

HEADERS = {"requesterId": "skynet"}

#######################

########### Read barcodes from all images in given directory
reader = zxing.BarCodeReader()

from os import listdir
from os.path import isfile, join
fileList = [UPC_DIR + "/" + f for f in listdir(UPC_DIR) if isfile(join(UPC_DIR, f))]

print("Files in Dir:");
print('[%s]' % ', '.join(map(str, fileList)))

rawBarcodes = reader.decode(fileList, True)
print ("barcodes detected:")

# Deduplicate and sanitize barcodes
rawBarcodes = list(set(rawBarcodes))
barcodes = [] # Now a list of strings, rather than barcode objects
for barcode in rawBarcodes:
  if isinstance(barcode.data, str):
    newCode = barcode.data.replace("\n", "")
    barcodes.append(newCode)

stringlist = ""
for code in barcodes:
  stringlist += code
print(stringlist)

###### Update Salesforce
# Utilize the middleware service to simplify
POST_URL = "http://localhost:8080/opportunities/v1/opportunity/"
for barcode in barcodes:
  retry = 0
  response = [];
  while retry < RETRY_COUNT:
    retry = retry + 1
    url = POST_URL + UPC_TO_OPPORTUNITY_MAP[barcode]
    request = {"Package_Id__c": barcode}
    # body = '{"Package_Id__c": "' + barcode + '"}'
    #print("Request body: \n" + body)
    response = requests.patch(url, json=request, headers=HEADERS)
    
    if response.status_code == 200:
      break
  else: 
    print("Staggering failure, out of retries")
  
  if response.status_code == 200:
    print("Updated Package_Id__c for Opportunity " + UPC_TO_OPPORTUNITY_MAP[barcode])
  
  

