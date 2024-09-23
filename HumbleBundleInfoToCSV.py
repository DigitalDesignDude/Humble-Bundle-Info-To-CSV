
page_url = input("Please enter or copy-and-paste the web address of the Humble Bundle page containing the items you wish to collect information for. All item details will be saved in a CSV spreadsheet file within the same directory from which this app was run:\n")

def CollectHumbleBundleItems(url):
    import requests
    import csv
    import time

    #Reduce warning messages in Command Prompt
    import warnings
    warnings.filterwarnings('once')
    
    # Selenium Library For Page Interaction
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    #Loop through common browsers until one is found on the user's device. Then use it for the web driver.  
    browsers = [webdriver.Chrome, webdriver.Edge, webdriver.Firefox, webdriver.Safari]
    driver = None

    for browser in browsers:
        try:
            driver = browser()
            break  # Exit loop if a browser is successfully launched
        except Exception as e: print("Error: ", e)


    # Get the bundle title from its url and format it to be more legiable
    bundle_title =  page_url.split('?')[0].split('/')[4].title().replace('-', ' ')

    print(f"\n!!! STARTING DATA COLLECTION FOR BUNDLE:\n {bundle_title} !!!\n")

    # Navigate to humble bundle page and wait for the user to continue the script once the page is fully loaded.
    driver.get(page_url)
    
    #SETUP CSV SPREAD SHEET ==================================================================================
    
    file_name = "Humble Bundle - " + bundle_title + ".csv"

    # Array to Store the CSV Data
    CSV_data = [] 
    
    #Create the .csv file 
    file = open(file_name, 'w', newline='', encoding='utf-8-sig')

    #Create a variable for writing to the csv
    writer = csv.writer(file)
    
    #clear the spreadsheet if the file already contains information
    file.truncate(0)
    
    #=========================================================================================================

    print("------------------------------------------------/n")

    #Variables used for CSV Row creation
    item_title_CSV = ""
    item_info_CSV = ""
    
    try:
        # Get the available tier titles and use them for the column headers of the CSV file.
        tiers = driver.find_elements(By.CLASS_NAME, 'js-tier-filter')
        tier_titles = [tier.text for tier in tiers]
        CSV_data.append(['Item Name', 'Description' ] + tier_titles)
        
        # For Each Tier filter that exists, click on the tier then store all the tier's items in the CSV file.
        for i in range(len(tiers)):
            print("START OF TIER: " + tiers[i].text)
            tiers[i].click() 
            time.sleep(3)
            
            #Go through and store all the items' info in CSV rows
            
            items = driver.find_elements(By.CLASS_NAME, 'tier-item-view')
            descriptions = driver.find_elements(By.CLASS_NAME, 'description')
            
            for k in range(len(items)):
                item_title_CSV = items[k].find_element(By.CLASS_NAME, 'item-title').text
                item_info_CSV = descriptions[k].get_attribute("textContent").strip()
                print("Title: " + item_title_CSV)
                print("Description: " + item_info_CSV + "\n")
                row_data = [None] * 20 # Redeclared between items to clear it and prevent issues. 
                row_data[0] = item_title_CSV
                row_data[1] = item_info_CSV
                row_data[i+2] = "✔"  

                #if the item title already exists in the CSV data, then update it with new info.
                duplicateFound = False
                r = 1 #skip checking the header row
                while r < len(CSV_data): 
                    if CSV_data[r][0] == item_title_CSV:
                        duplicateFound = True
                        CSV_data[r][i+2] = "✔" #add additional check to the proper row and column
                        break
                    r+=1
                if duplicateFound == False: 
                    # if not a duplicate, then append it to the rest of the CSV data                   
                    CSV_data.append(row_data)                    
                
                #Print CSV rows for debugging if needed
                #for row in CSV_data: print(row)            
                
    except Exception as e: print("Error: ", e)
            
    # Write the CVS data to the CSV File
    writer.writerows(CSV_data)

    # Close the CSV file
    file.close()

    print("\n!!! DATA COLLECTION COMPLETED !!!")

CollectHumbleBundleItems(page_url)