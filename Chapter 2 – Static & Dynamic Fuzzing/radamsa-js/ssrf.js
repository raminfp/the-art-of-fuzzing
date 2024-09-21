const child_process = require('child_process');
const radamsa = child_process.spawn('./bin/radamsa', ['-n', 'inf']);



radamsa.stdin.setEncoding('utf8');
radamsa.stdin.write("user:pass@domain.com:23/?ab=12#")
radamsa.stdin.end()

radamsa.stdout.on('data', function (input) {
    input = 'http://' + input

    //console.log("ookkokko");
    // Resulting host names need to be valid for this to be useful
    function isInvalid(host) {
        return host === null || host === '' || !/^[a-zA-Z0-9.-]+$/.test(host1);
    }

    let host1;
    try {
        host1 = new URL(input).hostname;
//	console.log(host1);
    } catch (e) {
        return; // Both hosts need to parse
    }

    if (isInvalid(host1)) return;
    if (/^([0-9.]+)$/.test(host1)) return; // host1 should be a domain, not an IP

    let host2;
    try {
	console.log("#########################################");
        host2 = require('url').parse(input).hostname;
	console.log(host2);

    } catch (e) {
        return; // Both hosts need to parse
    }

    if (isInvalid(host2)) return;
    if (host1 === host2) return;

    console.log(
        `${encodeURIComponent(input)} was parsed as ${host1} with URL constructor and ${host2} with url.parse.`
    );
});
