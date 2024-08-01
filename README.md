# Bulk Image Processor
 An application to streamline the bulk processing of images.

### About

test image link: https://drive.google.com/drive/folders/1J1XNUwHGQuAM23ET66IDhEb0Mgg-NuOL?usp=sharing
app link: https://drive.google.com/file/d/1XQx-nIv5bcNiQ6iurAlkbm4_Rmb3fbOZ/view?usp=sharing

As provided, the Bulk Image Processor can create segmentation masks for images, and apply those masks to produce
visualizations of those images.

The segmentation masks are produced using a VGG16 CNN pretrained on Khanhha's crack dataset. Details and the model can
be found at: https://github.com/khanhha/crack_segmentation/tree/master

The model can therefore detect cracks and structural integrity issues in buildings.

This application preprocesses the images before passing them through the model. The images can be split into an array of
smaller images, with the aim of receiving a more accurate model output.

The mask produced assigns a confidence value to each pixel in the image. The visualization section of the application
allows the user to provide a confidence cutoff, and overlay the mask on the source image in the user's choice of color.

The output images can then be used in photogrammetry.

### Dependencies
This application only works on computers running Windows, with a NVIDIA graphics card. 

If you have the bundled single-executable application file, no additional dependencies are required.

If you intend to run the Python code in a normal Python process, dependencies for this application can be found in
`requirements_conda.txt` and `requirements_pip.txt`, for conda and pip respectively.

Using the conda dependency list is
recommended, since the dependencies were installed using conda, and the pip dependency list does not include the
specific package builds, which is important to consider since pytorch-cuda is intended to be used.

You will also need to add the pretrained model within the `./vgg16_khanhha_related/models` directory.

This application is compatible with Python 3.11.9; I have not tested with other Python versions.

### Execution
To run the application in a Python process, run the `__main__.py` file. The application's GUI should appear shortly.
