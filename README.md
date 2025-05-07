### CS5330 Databases Project


# Testing Required (For you, Ani):

If something is off in testing, mark it down for the morning when we convene. This is based off Dr. Lin's reqs

## From Project Description
# Data Entry
- o Enter basic information into user, post, project, or record
- o Enter the set of posts that is associated with a project (We have a tab at the top for that called "Project"). Notice that if a post already exists, it should not be stored in the database multiple times.
- o For a project, entering the analysis result. System should allow partial results to be entered (We have a tab at the for this called "Update Record")
# Querying post (The 4 queries)
- o Find posts of a certain social media
- o Find posts between a certain period of time
- o Find posts that is posted by a certain username of a certain media
- o Find posts that is posted by someone with a certain first/last name
Condition: For each query, you should return the text, the poster (social media/username), the time posted, and the list of experiment that is associated with that post.
Also try combinations of these and make sure they still return correctly
# Querying experiment: 
Condition: You should ask the user for the name of the experiment, and it should return the list of posts that is associated with the experiment, and for each post, any results that has been entered. 
Also you need to display for each field, the percentage of posts that contain a value of that field.

## From Dr. Lin Rubric
# Data Entry: Test for
- Accepting incorrect input, these include (but are not limited to): 
  - Duplicate values when unique values are required two different people on the same social media cannot have the username for a project (should be built into schema)
  - A post received two different values for the same field
  - Invalid value supplied (a project analyzed a post that does not exist)
  - A post has a negative number of dislikes
- Rejecting valid input, these include (but are not limited to): 
  - The same username in two different social network can refer to two different people (should be built into schema)
  - A post can be associated with multiple projects (built into schema)
# Query post:
- All 4 queries should be correctly implemented (retrieval of all posts that satisfy the condition, and no post that doesn’t). Include cases where there is no post satisfying the query, and cases where there are multiple post that satisfy it.
# Query experiment:
- Need to retrieval the correct posts. Notice that not every post may have the same set of fields attached.

## From Tom (specific to our implementation)
- Check that the UI responses for the insertion and updating match up for the actual reponse (For ex: if it says it worked but you look in mysql workbench and it didn't work/there was an incorrect response)
- Make sure "Update Record" tab properly grabs the records and updates them
- Make sure "Project" tab properly shows posts and properly puts them into the record table given the proper inputs
- Anything else you think should be tested
