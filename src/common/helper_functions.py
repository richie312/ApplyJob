# -*- coding: utf-8 -*-
import os
# produce output decorator.
# def db_execution(func):
#     def inner1(*args, **kwargs):
#         # Initialize the directory
#         if not os.path.exists(os.path.join(data_dir,"output")):
#             os.makedirs(os.path.join(data_dir,"output"))
#         logger.info("Created the output directory.")
#         output_path = os.path.join(data_dir, "output")
#         # getting the returned value
#         df , filename = func(*args, **kwargs)
#         df.to_csv(os.path.join(output_path,filename))
#     return inner1
