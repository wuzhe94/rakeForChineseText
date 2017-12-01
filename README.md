# RAKE
Implementation of RAKE algorithm for Chinese text

- The implementation is based on python3.6, and use jieba package for Chinese word segmentation. 
  Please make sure you have installed the jieba package.
- For more details about RAKE algorithm, please refer to the original paper proposed by S. Rose, D. Engel, N. Cramer, W. Cowley.
  - https://pdfs.semanticscholar.org/5a58/00deb6461b3d022c8465e5286908de9f8d4e.pdf
- The effect of Chinese word segmentation has a great influence on the result of key phrases extraction, so if you want better results, it's better to use an advanced Chinese word segementation algorithm, not just use the jieba package.
- Stop words will also greatly affect the effect of key phrases extraction. In order to get satisfactory results, it's recommended to use a specific stop word list for specific domain, rather than using a general stop word list.
- Please note that the Chinese text should be utf-8 coded. 
  The key phrases extraction results of the sample Chinese txt are as follows, for reference only.
  - ![](https://github.com/wuzhe94/RAKE/blob/master/img/keyPhrases.jpg)
  
If there is any doubts, please feel free to contact me.
Zhe
wuzhe94@gmail.com
