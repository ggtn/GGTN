# TensorGNN

The implementation of paper "Tensor-based Gated Graph Neural Network for Automatic Vulnerability Detection in Source Code". This model is implemented in Python and applied to c/c++ source code vulnerability detection.

Codegraphs-tensor-master:
Based on the Joern code parser, the AST/CFG/DFG/NCS code graph is extracted, and the code node tokens sequence is converted into a low dimensional embedding vector using word2vec. The code graph tensor is constructed using the adjacency matrix of four code graphs and labeled with sample labels.

## 1. Datasets

## 1.1 Datasets download

1) All our datasets come from public papers. For more accurate experiments, we strongly recommend that you download the datasets according to the following url and set them:

[1] Lin G, Zhang J, Luo W, and et al. POSTER: Vulnerability Discovery with Function Representation Learning from Unlabeled Projects. In: Proceedings of the 2017 ACM SIGSAC Conference on Computer and Communications Security, CCS 2017, Dallas, TX, USA, October 30 - November 03, 2017. ACM; 2017. p. 2539–2541.

[2]  Li Z, Zou D, Xu S, and et al. VulDeePecker: A Deep Learning-Based System for Vulnerability Detection. In: 25th Annual Network and Distributed System Security Symposium, NDSS 2018, San Diego, California, USA, February 18-21, 2018.

[3] Russell RL, Kim LY, Hamilton LH, and et al. Automated Vulnerability Detection in Source Code Using Deep Representation Learning. In: 17th IEEE International Conference on Machine Learning and Applications, ICMLA 2018, Orlando, FL, USA, December 17-20, 2018. IEEE; 2018. p. 757–762.

[4] Zhou Y, Liu S, Siow JK, Du X, and Liu Y. Devign: Effective Vulnerability Identification by Learning Comprehensive Pro-
gram Semantics via Graph Neural Networks. In: Advances in Neural Information Processing Systems: Annual Conference
on Neural Information Processing Systems; 2019. p. 10197–10207.


2) We also upload our datasets of source codes and extrected datasets. Note that due to the space limitations, we cannot upload all datasets but most datasets used in our paper. This will drastically change the results of the experiment. 

Google Drive: [https://www.sri.inf.ethz.ch/research/plml](https://drive.google.com/file/d/1vAZrNPkIf0MAX5Q2bZZMqtdAT4TIeELL/view?usp=sharing)

## 1.2 Datasets descriptions
We use 13 kinds of CWE statistics

1. **CWE-120: Buffer overflow Description.** A buffer overflow condition exists when a program attempts to put more data in a buffer than it can hold, or when a program attempts to put data in a memory area outside of the boundaries of a buffer. Buffer overflows can be used for bypassing security services, causing program crashes and arbitrary code execution.
     
2. **CWE-125: Out-of-bounds Read.** The software reads data past the end, or before the beginning, of the intended buffer. This typically occurs when the pointer or its index is incremented or decremented to a position beyond the bounds of the buffer or when pointer arithmetic results in a position outside of the valid memory location to name a few. This may result in corruption of sensitive information, a crash, or code execution among other things.

3. **CWE-469: Use of Pointer Subtraction to Determine Size.** The product subtracts one pointer from another in order to determine size, but this calculation can be incorrect if the pointers do not exist in the same memory chunk. These types of bugs generally are the result of a typo.
   
4. **CWE-476: NULL Pointer Dereference.** A NULL pointer dereference occurs when the application dereferences a pointer that it expects to be valid, but is NULL, typically causing a crash or exit. NULL pointer dereference issues can occur through a number of flaws, including race conditions, and simple programming omissions.

5. **CWE-119: Buffer Errors.** The software performs operations on memory buffers, but it can read or write to memory locations outside the intended boundaries of the buffers. An attacker could execute arbitrary code, modify the intended control flow, read sensitive information, or cause a system crash.
   
6. **CWE-399: Resource Management Errors.** This type of vulnerability is related to improper management of system resources during software execution, such as, memory, disk space, files, etc.

7. **CWE-189: Numeric Errors.** This type of vulnerability is mainly caused by incorrect handling of numbers, such as integer overflow, sign error, division by zero, etc.

8. **CWE-362: Race Condition.** The program contains sequences of code that can run concurrently with other code and that require temporary, mutually exclusive access to shared resources. But there exists a time window within which another sequence of code can concurrently modify the shared resource. If the expected synchronization activity is located in safety-critical code, it may pose a security risk. 

9. **CWE-200: Information Exposure.** The information leak is the intentional or unintentional disclosure of information to someone who does not have access to that information. This type of vulnerability is caused by information leakage due to some incorrect settings in the software.
     
10. **CWE-17: Code problem.** This kind of vulnerabilities arise during the development of code, including the specification, design, and implementation of the software. 
   
11. **CWE-20: Improper Input Validation.** The product does not validate or incorrectly validates inputs that can affect the control flow or data flow of the program. When software fails to properly validate input, an attacker is able to forge input that is not expected by the application. This causes the system to receive some of the non-normal input, and an attacker could use the vulnerability to modify the control flow, control arbitrary resources, and execute arbitrary code.

12. **CWE-264: Permissions, Privileges, and Access Controls.** These vulnerabilities are those related to the management of permissions, privileges, and other security features used to enforce access control.

13. **Composited dataset.** We randomly collect some vulnerable functions from the above 12 kinds of vulnerabilities, and mix them as the ``Composited" dataset.

## 2. Model steps

### 2.1 Code graph tensor extraction

1.python3 get_ data_ by_ joern.py: call Joern built-in command to generate code attribute graph (CPG) for each function sample and store it in dot file.

2.python3 select_ functions_ dotfiles.py: filter the dot files generated by function samples, and remove the code attribute graph dot files of global functions <global> and inline functions.
  
3.python3 joernAnalysis-new-version.py: parse the function sample CPG, sort and split the ast/cfg/ddg code diagrams, give the leaf nodes to build NCS in sequence, and store the four code diagrams in the JSON file.

4.python3 create_ target_ for_ dataset.py: generate corresponding sample labels for the sorted source function samples, "1" indicates fragile samples, "0" indicates security samples; Generate a sample label dictionary "xxx.json", whose structure is {function_name:label}.

5.python3 extract_ graphs_ tensor.py: use the word2vec model to generate the node tokens embedding vector, convert the node type to a 1-bit digital label, and splice it with the embedding vector as the initial embedding of the node. The edge sets of the four code graphs are transformed into two-dimensional adjacency matrices to form code tensor features, and each sample is labeled to form an input data set for model training.
  
Notes: in each step above, pay attention to adjusting the storage path of input and output data according to the actual situation.
In step 5, you can configure the word2vec embedded vector length as required.
  
### 2.2 Model training
  
1. copy the generated code tensor feature data set to the circggnn master/dataset folder.

2. For parameter configuration of circgggnn model, see circggnn master/configurations json.

3. run the "python3 main.py -p" command to start model training, cut the samples in the ratio of 0.8:0.1:0.1, and use them for training, verification and testing respectively, and finally output the model test results. Run the "python3 main.py -ps" command to introduce the early stop mechanism to prevent over fitting.
