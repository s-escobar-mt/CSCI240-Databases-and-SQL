No modifications were made as the tables already satisfy 3NF. 

1NF – Satisfied in all table values being atomic, all rows made unique, and no repeated values over separate columns 

2NF and 3NF – All table use a surrogate key as a primary key and there are no dependencies between values other than with the primary key and only the primary key 

 

NOTE: 

Billing address may seem dependent on Mailing Address and vice versa in the given examples, but they are not always one to one, and making a separate billing information table to reference would overcomplicate the project. 