def Count(count, config):
    msg = "[+] Finished: Successfully collected "
    msg += f"{count} Tweets"
    if config.Username:
        msg += f" from @{config.Username}"
    msg += "."
    print(msg)
