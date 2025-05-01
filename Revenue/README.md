# Revenue Data Description

The data comes from [__DataSF__](https://data.sfgov.org/Transportation/SFMTA-Parking-Meter-Detailed-Revenue-Transactions/imvp-dq3v).

Since the data file is too big, we do not upload the data file onto Github. We can query it directly from the API.

### Important features:

| Column Name | Description | Type |
| --- | --- | --- |
| POST_ID | Unique identifier of meter | Text |
| PAYMENT_TYPE | How the customer paid, one of the following: CASH, CREDIT CARD, SMART CARD | Categorical |
| SESSION_START_DT | The date and time of the start of the meter session for this transaction by the customer | Date & Time |
| SESSION_END_DT | The date and time of the end of the meter session for this transaction by the customer | Date & Time |
| METER_EVENT_TYPE | Event type of the meter, one of the following: NS = New Session; AT = Addtional Time; SC = Status Change | Categorical |
| GROSS_PAID_AMT | The amount paid by the customer for this meter transaction | Number |

There are total 16958906 rows in the filtered data set, the records are general meters from 12/01/2019 00:00:00 to 12/01/2020 00:00:00.