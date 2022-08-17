# KWIX Recommend API

**version**: *1.0.0*

## default

*no description*

### *no summary*

*no description*

**route:** `/sign_up`

**method:** `POST`

**requestBody:** 

*application/json*

| name | type | required | description |
| ---- | ---- | -------- | ----------- |
| id | string | True |  |
| email | string | True |  |
| password | string | True |  |
| name | string | True |  |
| sex | integer | True |  |
| birthdayDate | integer | True |  |
| phoneNumber | string | True |  |



### *no summary*

*no description*

**route:** `/login`

**method:** `POST`

**requestBody:** 

*application/json*

| name | type | required | description |
| ---- | ---- | -------- | ----------- |
| email | string | True |  |
| password | string | True |  |



### *no summary*

*no description*

**route:** `/logout`

**method:** `GET`



### *no summary*

*no description*

**route:** `/input`

**method:** `POST`

**requestBody:** 

*application/json*

| name | type | required | description |
| ---- | ---- | -------- | ----------- |
| age | integer | True |  |
| sex | interger | True |  |
| height | integer | True |  |
| weight | integer | True |  |
| bmi | interger | True |  |
| during | interger | True |  |
| email | string | True |  |





### *no summary*

*no description*

**route:** `/recommend`

**method:** `POST`

**requestBody:** 

*application/json*

| name | type | required | description |
| ---- | ---- | -------- | ----------- |
| email | string | True |  |




## schemas

### SignUpBodyModel

| name | type | required | description |
| ---- | ---- | -------- | ----------- |
| id | string | True |  |
| email | string | True |  |
| password | string | True |  |
| name | string | True |  |
| sex | integer | True |  |
| birthdayDate | integer | True |  |
| phoneNumber | string | True |  |


### UnprocessableEntity

| name | type | required | description |
| ---- | ---- | -------- | ----------- |
| loc | array | False | the error's location as a list.  |
| msg | string | False | a computer-readable identifier of the error type. |
| type_ | string | False | a human readable explanation of the error. |
| ctx | object | False | an optional object which contains values required to render the error message. |


### LoginBodyModel

| name | type | required | description |
| ---- | ---- | -------- | ----------- |
| email | string | True |  |
| password | string | True |  |


### UserBodyModel

| name | type | required | description |
| ---- | ---- | -------- | ----------- |
| age | integer | True |  |
| sex | interger | True |  |
| height | integer | True |  |
| weight | integer | True |  |
| email | string | True |  |
| bmi | integer | True |  |
| during | integer | True |  |


### UserResModel
| name | type | required | description |
| ---- | ---- | -------- | ----------- |
| email | string | True |  |
| name | string | True |  |
| id | string | True |  |
| height | integer | True |  |
| weight | integer | True |  |
| sex | interger | True |  |
| age | integer | True |  |
| bmi | integer | True |  |
| during | integer | True |  |



### RecommendBodyModel

| name | type | required | description |
| ---- | ---- | -------- | ----------- |
| email | string | True |  |


