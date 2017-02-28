# Commit Service application

## Provides the following functionalities
1. An endpoint for someone to post a secret message. The message would be identified as being posted by this person and will have the time at which it was generated in UTC time. We will refer to the secret message as a 'commitment'.
2. Each commitment posted by a committer will have 
    - a unique ID
    - username of the commiter
    - 'commitment value', which will be a unique random sequences of bytes that will not reveal any information about the message itself.
3. Each commitment will not have the message accesible, until a 'reveal' request is posted by the committer and the message becomes readable by everyone.
4. The committer of a given message will be able to reveal the message to everyone by calling an endpoint that would be accessible only to the committer.
5. The 3rd party (Eveyone other than the committer) can view the commitment posted by a committer using the commitment_value generated in step 2.
6. The 3rd party can call a 'verify' endpoint on a given message in order to verify that a message has not been changed since the time it was posted.

## Assumptions:
1. The communication with the service would be over https.
2. We assume here that the service itself is not 'compromised', i.e the committer and the 3rd party trust the service itself but don't trust each other.
4. For this exercise there will be no fine-grained control over which 3rd party can view messages of which commiter, i.e. there will not be any groups w.r.t third parties and committers. Everyone else except the owner of the message will be considered a 3rd party.

## Tools/Frameworks used:
1. Ubuntu 16.04 VM running on a AWS EC2 instance.
2. Python for the backend with Django web framework version 1.10 (latest stable)
3. sqlite DB that comes along with Django. This is was just for ease testing. For production a more robust DB like PostgreSQL, MySQL etc should be used.
4. Django REST framework to work with REST api endpoints.
5. cURL and Advanced REST Client for functional testing.
6. Django REST testing framework for unit and integration testing.

## Instructions on how to run
1. Clone the git directory on your workspace. `git clone https://github.com/vinay-pad/commit_service.git`
2. Navigate to commit_service directory `cd commit_service` and run,
    - Create a new virtual environment, `virtualenv .`
    - Activate the virtual environment, `source /bin/activate`
    - Install the dependancies specified in requirements.txt `pip install -r requirements.txt`
3. Navigate into the `src` directory and run `python manage.py runserver 0.0.0.0:8000`. This will run the server on port 8000 on your local box.
4. The project currently has DEBUG=True in the settings.py file which might print verbose errors when you run a unsupported/invalid curl request. This flag is kept as it is just for debugging and will be set to False in production.
5. Test the below endpoints using cURL or any other REST client.
6. **Important Note**
    - Some of the below endpoints are protected and require token based authentication.
    - I have checked in the db.sqlite3 file as well which already contains 2 users created for testing. You can obtain tokens for these users using the API,
 
    * `GET /v1/users/login/?username=test&password=test1234` or `GET /v1/users/login/?username=vinay&password=vinay123`
    * This request will return a token that needs to be sent as a authorization header like this `Authorization: Token 69e76dc16a64af8c765f0cc6015c815b963c339b`
    * There is a signal handler in 'users' app that will create a new token whenever `python manage.py createsuperuser` command is run.
    - This is a highly unsecure way of sharing a DB but this is just to make testing easier :) Just calling it out here.

## Endpoints:
Endpoints 1. and 4. will require a 'Authorization token' to be sent in the header in order to verify the user accessing these endpoints. Any endpoint accessed without the 'Authorization token' will be deemed as being accessed by a 3rd party.

- GET v1/users/login?name=<username>&password=<password>
- GET v1/commitments/
- POST /v1/commitments/
- GET /v1/commitments/<id>/
- POST /v1/commitments/<id>/readability/
- GET /v1/commitments/<id>/verification/

An explanation of each of the above endpoints is given below,

1. Get user token
    ```
    GET /v1/users/login?name=<username>&password=<password>
    returns `200 OK`
    {
        "token": <user-token>
    }

    ```

2. Get list of all commitments. 
    ```
    GET /v1/commitments/
    returns `200 OK` with a tuple of
            {
                'id': <unique-commit-id>
                'user': <username-of-committer>,
            }
    ```

3. Create a new commitment. Throws a `401 Unauthorized error` if a valid auth token isn't passed in the header
    ```
    POST /v1/commitments/  with 'Authorization token' in the header and POST params 'message=<secret-message>'
    returns `201 Created`
        {
            'id': <unique-commit-id>
            'user': <username-of-committer>,
            'message': <created-message>,
            'created_ts': <created-timestamp>
        }
    ```

4. Get details of a particular commitment 
    ```
    GET /v1/commitments/<id>/
        returns `200 OK` if the resource exists with below response
            {
                'id': <unique-commit-id>,
                'user': <username-of-committer>,
                'commit_value': <commitment-value>
            }
        if this commit hasn't been made readable yet.

        returns `200 OK` if the resource exists with below response
            {
                'id': <unique-commit-id>,
                'user': <username-of-committer>,
                'commit_value': <commitment-value>
                'message' : <secret-message>,
                'created_ts': <created-timestamp-of-secret-message-in-utc>'
            }
        if this commit has been made readable.

    ```

5. Irrevocably reveal a commitment to everyone
    ```
        POST /v1/commitments/<commit-id>/readability/ with 'Authorization token' in the header. This doesn't take any POST params. It just creates a 'readability' singleton instance and associates it with the commitment. This action is irreversible because the only action allowed on this endpoint is 'POST'.
        returns `201 Created`
            {
                'commitment': <commit-id>,
                'readable': "True"
            } 
        if this is the first time this endpoint is being called.

        returns `200 Ok`
            {
                "detail": "Request to make message readable successful"
            }
        when called subsequent times, without making any changes to the resource
    ```

6. Verify when a message was posted and that it has not been tampered with since then
    ```
        GET /v1/commitments/<id>/verification/
        returns 
        {
            'id': <unique-commit-id>,
            'user': <username-of-committer>,
            'commit_value': <commitment-value>,
            'created_ts': <created-timestamp-of-secret-message-in-utc>,
            'tampered': <true-or-fasle>
        }
    ```

## Algortihms used
1. In order to create a commitment value, SHA256 digest scheme is used in order to create a digest from the secret message, created timestamp and the user's authtoken. This ensures uniqueness and binding property of the message to the user and the time at which the message was created.

2. The 'hiding' property is achieved by not exposing the message through the GET endpoint until the commitment is 'revealed'.

3. Irrevocability of the revealing the messages is ensured by having a singleton object generated during the revealing phase that cannot be changed, updated or deleted by anyone including the committer himself.

4. The actions allowed on the exposed endpoints is restricted only to the allowed ones on that endpoint so that an adversary does not try to use an endpoint in ways that it is not supposed to be used. For example, PUT/PATCH/DELETE is not allowed on the commitment endpoint and PUT/PATCH/DELETE is not allowed on the 'readability' singleton object etc.

5. Verification that the message has not been tampered with since generation of the message is done by generating a commited_value from the message, created_ts and user id and ensuring that its equal to the stored commitment value.

6. The user is authenticated using a token that is generated once using his username and password. It is not ideal to re-use the same token everytime, instead it should expire within a certain amount of time and we should be generating new tokens.

## Known Vulnerabilities
1. The SHA256 digest created ensures uniqueness to a given message, user and timestamp but an adversary with unbounded computing capabilities can generate repeatedly run the hash function of changing inputs in order to recover the secret message.

2. The service itself is assumed to be not compromised, if it is compromised then the secret messages will be known to the adversary. One way to avoid this is to **encrypt** the secret messages using the user's token. The token of the user himself should not be stored in the system in such a case and the token needs to have lifetimes that expire within a period of time.

3. If the adversary knows that the digest is computed on the concatenation of messge, timestamp and userid, it narrows down the possibility of guesses of the message.

4. Since we don't support DELETE of commitments, system can get overwhelmed with create commitment requests and commitments can get created unboundedly.

## Unit and Integration Testing
1. Django REST testing framework was used to run unit/integration tests for the following user flows,
    - These tests can be found at `src/commitments/tests.py` and instructions on how to run it are as below,
    ```
        export TEST_SERVER=<set-this-to-your-server>
        export TEST_USER=<username>
        export TEST_PWD=<pwd>
        cd to src/
        python manage.py test
    ```
    Sample output,
    ```
    (commit_service) ubuntu@ip-172-31-12-203:~/commit_service/src$ python manage.py test
    Creating test database for alias 'default'...
    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 0.232s

    OK
    ```

    ### Flow 1 - verify secrecy of message
    1. User login and gets token.
    2. User creates a commitment.
    3. Verify commitment is accessible via the commit-id
    4. Verify commitment's message is not visible in the GET /v1/commitments/<id>/ endpoint.
    
    ### Flow 2 - verify message can be revealed only once irrevocably.
    1. Repeat steps 1 to 4 from Flow 1.
    2. POST to the readability endpoint to make the message readable.
    3. Repeat step 2 and verify it doesnt change anything in the resource.

    ### Flow 3 - verify message hasn't been tampered with since creation
    1. Repeat steps 1 to 4 from Flow 1.
    2. Call the verification endpoint and verify that the 'tampered' flag is false.
