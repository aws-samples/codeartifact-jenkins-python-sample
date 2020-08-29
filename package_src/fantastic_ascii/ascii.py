# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

def joe_say(text):
    template = r'''
    =-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=
    // {message}    \\
     =-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=
       \\
        \\
           ----------------
          /                \
         /                  \
        |     OO      O0     |
        |     OO      OO     |
         \         -        /
          \     DDDDDD     /
           \     DDDD     /
            \____________/
    '''.format(message=text)

    return template
