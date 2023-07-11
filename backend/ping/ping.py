from ping3 import ping

# Return the time for response, if -1 request is timed out, if -2 cannot resolve url
def ping_url(url, timeout=10):
	res = ping(url, timeout=timeout, unit="ms")
	
	# It means cannot resolve
	if res == False:
		return -2
	
	# It means timed out
	if res == None:
		return -1
	
	return res

# Test cases
test_cases = [
    "example1.com",
    "example2.com",
    "example3.com",
    # Add more test cases as needed
]