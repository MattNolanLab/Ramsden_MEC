#ABA Registration Pipeline

Accompanies the paper entitled "Laminar and Dorsoventral Molecular Organization of the Medial Entorhinal Cortex Revealed by Large-scale Anatomical Analysis of Gene Expression"

Helen L. Ramsden, Gülşen Sürmeli, Steven G. McDonagh and Matthew F. Nolan

## Notes

The Ipython notebook and accompanying files contain the workflow for registering images using the ABA. 

Each code block in the notebook should be able to be run independently in a particular session, though of course some depend on others having been run at some point in the past (such as image download).

Some elements were run using Matlab, other scripts call ImageJ (where indicated) so you will need to have these installed on your computer, and you will also need to specify the path to them.

The only stage that is very difficult to run on a desktop computer is group registration.

The Example_Results folder contains the results of an example run with just 10 images. For this run we started with a list of genes of interest and our group-registered images for each section.

Please email helenlram [at] zoho [dot] com if you have any queries.

## Licence

Copyright (c) 2014, Helen Ramsden
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.