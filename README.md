# MigrateOllamaModels
An utility to migrate Ollama Models to another location.

# How to use 
Suppose you have an existing folder containing the Ollama models:

```
~/.ollama
    |__models
         |__blobs
               |__ ....
               |__ ....
         |__manifests
               |__registry.ollama.ai
                      |__library
                            |__deepseek-r1
                                 |__1.5b
                                 |__7b
                            |__llama3.2
                                 |__latest
                            |__mxbai-embed-large
                                 |__latest
```

Here the original root of the Ollama models folder is `~/.ollama/models`. 

Say you now want to shift all the models to your external SSD. 

To do that, you can add the following statement to the .zshrc file:

```
export OLLAMA_MODELS="/Volumes/SSD2/ollama"
```

So now the destination root of the Ollama models folder is `/Volumes/SSD2/ollama`.

You can now run the utility in Terminal:    

**MigrateOllamaModels.py**

```
$ python MigrateOllamaModels.py

Enter the root path of the Ollama models folder: ~/.ollama/models                 <-----enter this
Enter the destination root path of the Ollama model folder: /Volumes/SSD2/ollama  <-----enter this

Enter the name of the model (or 'exit' to quit): llama3.2                         <-----enter this
Enter the version of the model: latest                                            <-----enter this

Digest values found in ~/.ollama/models/manifests/registry.ollama.ai/library/llama3.2/latest:  
  sha256:34bb5ab01051a11372a91f95f3fbbc51173eed8e7f13ec395b9ae9b8bd0e242b  
  sha256:dde5aa3fc5ffc17176b5e8bdc82f587b24b2678c6c66101bf7da77af9f7ccdff  
  sha256:966de95ca8a62200913e3f8bfbf84c8494536f1b94b49166851e76644e966396  
  sha256:fcc5a6bec9daf9b561a68827b67ab6088e1dba9d1fa2a50d7bbcc8384e0a265d  
  sha256:a70ff7e570d97baaf4e62ac6e6ad9975e04caa6d900d3742d37698494479e0cd  
  sha256:56bb8bd477a519ffa694fc449c2413c6f0e1d3b1c88fa7e3c9d88d3ae49d4dcb  

Copied: sha256-34bb5ab01051a11372a91f95f3fbbc51173eed8e7f13ec395b9ae9b8bd0e242b to /Volumes/SSD2/ollama/blobs  
Copied: sha256-dde5aa3fc5ffc17176b5e8bdc82f587b24b2678c6c66101bf7da77af9f7ccdff to /Volumes/SSD2/ollama/blobs  
Copied: sha256-966de95ca8a62200913e3f8bfbf84c8494536f1b94b49166851e76644e966396 to /Volumes/SSD2/ollama/blobs  
Copied: sha256-fcc5a6bec9daf9b561a68827b67ab6088e1dba9d1fa2a50d7bbcc8384e0a265d to /Volumes/SSD2/ollama/blobs  
Copied: sha256-a70ff7e570d97baaf4e62ac6e6ad9975e04caa6d900d3742d37698494479e0cd to /Volumes/SSD2/ollama/blobs  
Copied: sha256-56bb8bd477a519ffa694fc449c2413c6f0e1d3b1c88fa7e3c9d88d3ae49d4dcb to /Volumes/SSD2/ollama/blobs  
Copied: 'latest' file to /Volumes/SSD2/ollama/manifests/registry.ollama.ai/library/llama3.2  

Do you want to process another model? (yes/no):
```

If you type yes, you can specify another model and version to migrate.
