Asynchronius bot for telegram channel with memes.


Requires: python 3.7+


Work scheme:
```
                                             +---->>>>>(send approved meme)>>>>>----Channel with memes
                                             |
                                          +-----+
                    Private chat ----+--->| Bot |---->>>>(send meme and poll)>>>>----Moderate group
Send image--->>>---|                 |    +-----+                                        |
                    Group chat ------+       |                                           |
                                             +--------<<<<<<(send response)<<<<<<--------+

```
