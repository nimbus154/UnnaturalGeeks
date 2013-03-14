## User
* Username (unique identifier)
	* email address
* Password
	* Hashed and salted password
 	* sha-256
* Salt

## Job
* Unique ID
* Job Title
* Company
* Job Post URL
	* Description of position
* Copy of Job Post/Description
* Applied Date
* City
* State
* Notes

## Contact
* Associated Job ID
* Contact Name
* Email
* Phone
* Notes

## Document (Resume, Cover letter)
* Document ID
* Date Uploaded
* Blob of document
* Mime Type (Internet media type)
* Description
* Document type (resume, cover letter, other)
	* Should be an enum, if available
* Associated Job (FK)

## Correspondences
* FK to Job
* FK to Contact (Optional)
* Date of Correspondence
* Correspondence
