# gen1-azure-datalake-access-example
An example to download files from gen1 datalake from Azure

This project is an example in Python of how to access the gen1 azure datalake.

More than that, it's a way to download some files from it. In our cases, these files are "picke" machine learning models.

Suppose, we have 3 models. Each model is a folder of 3 files: 2 texts and 1 binary (the one named "model.pkl").

So, we have a file tree like that:

- Model1
  - model.pkl
  - otherfile.txt
  - otherfile2.txt

- Model2
  - model.pkl
  - otherfile.txt
  - otherfile2.txt
  
  
- Model3
  - model.pkl
  - otherfile.txt
  - otherfile2.txt
 
 We want to download them the same way. This is what this small project is about.
 
 We use the RestAPI to access a gen1 datalake.
 
 **Note: It's not possible to download the files with this RestAPI. So, we copy the content of each file in local files.**
