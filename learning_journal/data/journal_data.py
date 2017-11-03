"""Mark writes journals and saves them."""


FMT = '%m/%d/%Y'
BLOGS = [
    {
        "id": 12,
        "creation_date": "2017-11-01T03:33:50.617870",
        "title": "Day 12 Journal",
        "author": "Mark Reynoso",
        "body": "There is so much in my brain right now. Yesterday's work was filled with unexpected and peripheral hangups that kept me from even looking at our portfolio work for today. The material seems like a lot of details to keep track of and it's all a bit overwhelming. I am very excited for my team project and for our attempt to learn some machine learning."
    },
    {
        "id": 11,
        "creation_date": "2017-10-30T23:46:53.303767",
        "title": "Day 11 Journal",
        "author": "Mark Reynoso",
        "body": "Seeing all the work we did last week to build a server get done in pyramid/cookiecutter is just a few lines was both exciting, because we don't need ot build another server from scratch, and sad because it was so much sweat and tears for something that is valuable but not so useful. However, as we did code review I was pleased that things were starting to make sense because last week there were some really dark moments. At the same time, the idea of learning new packages as large and complex as pyramid and django was a bit much, but I'm ready for another challenget this week!\r\n\r\nStarting to think about mid-term projects was great. I was certainly not ready to plan for a project, it feels like we just started, but it was great to think about what we might start investing our energy in."
    },
    {
        "id": 10,
        "creation_date": "2017-10-28T05:41:49.120679",
        "title": "Day 10 Journal",
        "author": "Mark Reynoso",
        "body": "Servers. Sockets. Ugh. It's amazing how little I seemed to know going into the step3 assignment. I've read a lot of docs and learned about os. But it's still pretty hazy. I feel like this was the biggest challenge for me in a while, so it was bittersweet. Yay servers!"
    },
    {
        "id": 9,
        "creation_date": "2017-10-27T05:49:04.829651",
        "title": "Day 9 Journal",
        "author": "Mark Reynoso",
        "body": "What is CSS? HTML? Ha, after trying to go and starting building out my own journal page I realized how quickly the details of those skill go away. Fortunately it came back quickly. And, I edited some JS problems on my portfolio page that have need some attention. After doing this I felt much better about my knowledge of all that front end stuff and enjoyed it. But, how in the world do I make forms work without JS and jQuery!?"
    },
    {
        "id": 8,
        "creation_date": "2017-10-26T03:40:02.469302",
        "title": "Day 8 Journal",
        "author": "Mark Reynoso",
        "body": "The white board challenge today was great. I walked away from that feeling like I have good handle on linked lists so far and set a good tone for the rest of the day. I'm beginning to feel some clarity in some of the concepts we've been learning. One of the pieces of the linked list that made conceptual sense in the white board was the idea of a random things that point to one another rather than a large thing that is all connected. It was hard not to think of a linked list as a kind of list with list properties. But in trying to traverse and zip list the fact that there are simple a bunch of nodes with pointers clicked."
    },
    {
        "id": 7,
        "creation_date": "2017-10-25T04:32:41.686362",
        "title": "Day 7 Journal",
        "author": "Mark Reynoso",
        "body": "Finding something in a string became infinitely easier today. 'string' in 'somestring' is True. Um, is it supposed to be that easy? Thank you, Python. Also, I learned during testing that you can't return a string. Then when getting help from a TA he encouraged me to return the string for testing. After trying it many times and receiving an error, it worked. We don't know why it wouldn't do it previous to that. I'm assuming it was magic, but it may have been an error on our part...maybe."
    },
    {
        "id": 6,
        "creation_date": "2017-10-24T04:23:59.020018",
        "title": "Day 6 Journal",
        "author": "Mark Reynoso",
        "body": "Learning seems like a term that would indicate that I know something based on the work today. I certainly took in a lot of information, but I don't know how many dots are connected yet. Using an else statement on a while loop was great."
    },
    {
        "id": 5,
        "creation_date": "2017-10-21T21:47:43.261518",
        "title": "Day 5 Journal",
        "author": "Mark Reynoso",
        "body": "Environments will be the death of me. Typos will be the death of me. Tox will be the death of me. And, then I'll have time to learn how to code in python. The code wars challenge was great and I enjoyed the extra practice in small scale functions, but I ran into many problems getting my tests to run in tox. After much struggle, I think I got it (ish)."
    },
    {
        "id": 4,
        "creation_date": "2017-10-21T00:55:05.496177",
        "title": "Day 4 Journal",
        "author": "Mark Reynoso",
        "body": "I remember going to Mexico to visit my family as a kid and being totally overwhelmed by my inability to communicate with them. We were family, we had this deep connection and many things in common and yet we couldn't talk because our words made no sense to one another. That's similar to how it feels to work on code in Python. As we step into this new language, the concepts are familiar but the ability to communicate it in code is clunky. I really is not the same language. Today I was pumped that the environments began to make some conceptual sense. Baby steps."
    },
    {
        "id": 3,
        "creation_date": "2017-10-20T03:32:22.491392",
        "title": "Day 3 Journal",
        "author": "Mark Reynoso",
        "body": "Writing tests for my code necessarily changed the way the code was written, presumably for the better. Writing tests has forced the issue of clean code without my actual intent on writing clean code. What started out as a large mess was eventually cleaned up because the idea of writing a test for such a convoluted mess would have been impossible. This is twice that tests have had a positive impact on my coding. So far I am sold on testing, even if it is tedious."
    },
    {
        "id": 2,
        "creation_date": "2017-10-18T00:13:47.869590",
        "title": "Day 2 Journal",
        "author": "Mark Reynoso",
        "body": "Tests have satisfied my need for immediate results. Without a console to see the fruit of my labor, Python felt a bit unsatisfying. After writing some code and sending it off into the terminal abyss without a visual representation of what happened, if it happened, or what it did, it felt a bit like dumping my dinner down the garbage disposal. Tests provided the confirmation that the thing worked, or didn't. They allowed us to try things and attempt to break the code, and when those precious words 'passed' graced the screen we celebrated with a first bump and commit. I am sold on having a commitment to testing."
    },
    {
        "id": 1,
        "creation_date": "2017-10-16T22:31:09.906763",
        "title": "Day 1 Journal",
        "author": "Mark Reynoso",
        "body": "I'm lamenting the loss of the console in Chrome and Atom editor. These were familiar and comfortable lands in the world of my computer universe. Things made sense and gave me a metaphorical cushion to lay my overwhelmed brain. While concepts still seem familiar, the newness of the environments and syntax, though simple enough, have ripped from me the safety nets that helped me along. I'm ready to learn now."
    }
]
