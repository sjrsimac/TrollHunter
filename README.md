# TrollHunter
This is a reddit bot, written in Python, that uses machine learning to identify trolls.

TrollHunter measures three traits for each post.

* The difference between an author's age and his karma level. This is designed to catch trolls that have a bank of accounts that are old enough to get past age filters, but have almost no karma because the accounts have been sitting idle, just waiting to be used.
* The variety of words in a post. This measure is called Lexical Diversity, and it's defined as the number of unique words in a post divided by the total number of words in a post.
* How much formatting is used in the post. TrollHunter looks for lists, headers, bolded words, italicized words, and horizontal lines.

After collecting this information, TrollHunter checks for *moderator* reports of 'Trolling'. When TrollHunter finds a moderator report that indicates trolling, it quietly removes the item and makes a note in its logs that the removed post is the work of a troll. As Troll Hunter learns more and more about which posts are trolls, its ability to detect more trolls will improve.

For now, TrollHunter is in 100% observation mode, and it's going to observe us. Until now, our policy for troll posts has been quietly removing them from the site and noting the troll in the usernotes. TrollHunter demands one change to that plan: you will no longer remove trolling posts, but [file a report of 'Trolling' in the modqueue](https://goo.gl/photos/hqd1FGVLcJ1VWQXX7). This will tell TrollHunter which posts are trolls, and it will remove every post you report as trolling. If you report a comment as trolling, TrollHunter will remove the comment, but it will not log anything.

##Known Problems

* How will we handle posts that are deleted by the user?
* How will we handle authors that their accounts, but not the post?
