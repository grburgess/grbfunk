[![Build Status](https://travis-ci.com/grburgess/grbfunk.svg?branch=master)](https://travis-ci.com/grburgess/grbfunk)
[![codecov](https://codecov.io/gh/grburgess/grbfunk/branch/master/graph/badge.svg)](https://codecov.io/gh/grburgess/grbfunk)

# GRB Funk

Broadcasting mad GRB vibes to your earholes... well your phone holes. Thanks to *amazing* era of multi-messenger astronomy, the original [GCN](https://gcn.gsfc.nasa.gov) system's email distribution has made my email useless for following GRB alerts. Thus, I made this little tool to bump things to telegram thanks to the [pygcn](https://github.com/lpsinger/pygcn) package. 

**grbfunk** is highly customized for what I want to see, but fell free to use it as your own model.

## Installation

pip install grbfunk

## Usage

Note that this **will not** work out of the box as it looks for a telegram bot token and chat_id to transmit the messages. Of course, you do not have to use the software this way as it can serve as a clean wrapper around GRB notifications or as a backend pipeline. However if you desire to use it as is, you need a telegram bot and then:

```bash

	$> mkdir ~/.grbfunk
	$> cd ~./grbfunk
	$> touch access.yaml
	$> emacs access.yaml

```

```yaml

token:
	<your bot token>
chat_id:
	<your chat_id>


```

**Note:** if you do not use emacs this will still work. Unless you use vim. You should never do that. 

Then you can simply run

```bash
	$> grbfunk
```

and this will listen for GRB alerts and broadcast their funk to telegram. 
