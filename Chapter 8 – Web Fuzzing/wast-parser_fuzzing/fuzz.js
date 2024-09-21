const wast = require("@webassemblyjs/wast-parser");
function fuzz(buf) {
    try {
	wast.parse(buf)

    } catch (e) {
        // Those are "valid" exceptions. we can't catch them in one line as
        // jpeg-js doesn't export/inherit from one exception class/style.
            throw e;
    }
}

module.exports = {
    fuzz
};
