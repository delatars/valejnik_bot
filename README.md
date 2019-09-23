Asynchronius bot for telegram channel with memes.


Requires: python 3.7+


Work scheme:
```
                                             +---->>>>>(send approved meme)>>>>>----channel with memes
                                             |
                                          +-----+
                    Private chat ----+--->| Bot |---->>>>(send meme and poll)>>>>----moderate group
send image--->>>---|                 |    +-----+                                        |
                    Group chat ------+       |                                           |
                                             +--------<<<<<<(send response)<<<<<<--------+

```
