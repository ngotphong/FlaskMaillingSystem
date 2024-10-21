from getCSV import getCSV
from getGoogleDoc import downloadGoogleDocAsHTML, getPlaceholders, replacePlaceholders
from sendingEmail import authenticateGmail, sendEmail


def findEmailRow(data):
    for row in data:
        for item in row:
            if item == "Email" or item == "email":
                return data.index(row)


def customHTMLEmail(docURL=None, sheetURL=None, sheetTitle=None, subject=None):
    try:
        data = getCSV(googleSheetURL=sheetURL, sheetTitle=sheetTitle)
        htmlContent = downloadGoogleDocAsHTML(docURL=docURL, file=True)

        emailRow = findEmailRow(data=data)

        emailColumnIndex = data[emailRow].index("Email") or data[emailRow].index(
            "email"
        )
        columnIndexes = {"Email": emailColumnIndex}
        for fillIn in getPlaceholders(htmlContent=htmlContent):
            index = data[emailRow].index(fillIn) or data[emailRow].index(fillIn.lower())
            columnIndexes[fillIn] = index

        creds = authenticateGmail()

        for row in data[(emailRow + 1) :]:  # Skipping the header row
            userData = columnIndexes.copy()
            for key, index in columnIndexes.items():
                userData[key] = row[index]

            print(userData)

            # Make a fresh copy of the original HTML content for each email
            emailContent = htmlContent

            # Replace placeholders in the copied emailContent, not the original htmlContent
            emailContent = replacePlaceholders(
                htmlContent=emailContent, replacementDict=userData
            )

            # Send the email with the modified emailContent
            sendEmail(
                creds=creds,
                to=userData["Email"],
                subject=subject,
                htmlContent=emailContent,
            )

    except Exception as error:
        print(f"An error orcurred: {error}")


# def basicEmail(docURL=None, sheetURL=None, sheetTitle=None, subject=None, option="to"):
#     try:
#         data = getCSV(googleSheetURL=sheetURL, sheetTitle=sheetTitle)
#         htmlContent = downloadGoogleDocAsHTML(docURL=docURL, file=True)

#         emailColumnIndex = data[0].index("Email") or data[0].index("email")

#         creds = authenticateGmail()

#         if option == "to":
#             for row in data:
#                 sendEmail(
#                     creds=creds,
#                     to=row[emailColumnIndex],
#                     subject=subject,
#                     htmlContent=htmlContent,
#                 )
#         # elif option == "cc":

#     except Exception as error:
#         print(f"An error orcurred: {error}")


# docURL = input("Please input your Google Doc URL: ")
# sheetURL = input("Please input your Google Sheet URL: ")
# sheetTitle = input("Which sheet do you want to read(title): ")

# docURL = "https://docs.google.com/document/d/1D0bZ22qu7qxx6pnXq5bPBhRLKHkdOsPnTP2ziDF_J74/edit?usp=sharing"
# sheetURL = "https://docs.google.com/spreadsheets/d/1vaKcL1u4031p7CbywG6_Yg4mLDGyU4AY3rUWNErj05E/edit?usp=sharing"
# sheetTitle = "Sheet4"

# customHTMLEmail(
#     docURL=docURL,
#     sheetURL=sheetURL,
#     sheetTitle=sheetTitle,
#     subject="Full Tutorial cách để cook một website.",
# )
