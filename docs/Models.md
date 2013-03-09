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

## Resume
* Resume ID
* Date Uploaded
* Blob of cover letter
* Description
* Job FK

## Cover Letter
* Cover letter ID
* Date Uploaded
* Blob of cover letter
* Description
* Job FK

## Correspondences
* FK to Job
* FK to Contact (Optional)
* Date of Correspondence
* Correspondence
