# TrollHunter
This is a reddit bot, written in Python, that uses machine learning to identify trolls.

TrollHunter measures the following traits for each post. This list is not exhaustive because TrollHunter is under active development.

* The difference between an author's age and his karma level. This is designed to catch trolls that have a bank of accounts that are old enough to get past age filters, but have almost no karma because the accounts have been sitting idle, just waiting to be used.
* The variety of words in a post. This measure is called Lexical Diversity, and it's defined as the number of unique words in a post divided by the total number of words in a post.
* How much formatting is used in the post. TrollHunter looks for lists, headers, bolded words, italicized words, and horizontal lines.

After collecting this information, TrollHunter checks for *moderator* reports of 'Trolling'. When TrollHunter finds a moderator report that indicates trolling, it quietly removes the item and makes a note in its logs that the removed post is the work of a troll. As Troll Hunter learns more and more about which posts are trolls, its ability to detect more trolls will improve.

For now, TrollHunter is in 100% observation mode. To tell TrollHunter to note a post as the work of a troll, [file a report of 'Trolling' in the modqueue](https://goo.gl/photos/hqd1FGVLcJ1VWQXX7). TrollHunter will remove every post you report as trolling while noting its traits. If you report a comment as trolling, TrollHunter will remove the comment, but it will not log anything.

## Open Problems

* How will we handle posts that are deleted by the user?
* How will we handle authors that their accounts, but not the post?
