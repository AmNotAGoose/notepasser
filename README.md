# notepasser

## video demo
https://youtu.be/G_Q85QDvGYc

## update 2
added GUI, improved the code quality a lot, fixed lots of bugs

## what is it
a library allowing you to discover and send encrypted messages to people on your same network.

## features
- discover users on the same network
- send encrypted messages (NOT mitm resistant in the slightest)
- connect across different clients
- (future) have a preset rotating token which resets together at the start of each session
- gracefully connect and disconnect

## installation and running 
- install by `pip install notepasser`
- now you can run the follwing scripts
  - notepasser-cli: for cli client
  - notepasser-ui: for gui client
  - notepasser-fakecli: a secondary fake cli client which binds to home dir / .fakenotpasser, allowing you to test the application. this is considered a seperate user from the other 2 client options.
- now you can communicate to others which also run this client on different devices on the same network!
- for testing functionality on local computers:
  - run either notepasser-cli or notepasser-ui
  - run notepasser-fakecli. this is essencially the same as a secondary 'account' binded to home dir / .fakenotpasser.

## ai notice for siege
- main script used lots of help from ai but the core is written by myself completely (still holds very true)
- this week's update written without ai
- ai used to debug and fix packaging issue