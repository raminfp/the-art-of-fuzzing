const decompress = require('decompress');


function fuzz(buf) {
    try {
	//if (buf)
	decompress(Buffer.from(buf,'hex')).catch((err)=>{console.log(err)})
    } catch (e) {
        // Those are "valid" exceptions. we can't catch them in one line as
        // jpeg-js doesn't export/inherit from one exception class/style.
	 throw e;
    }
}

module.exports = {
    fuzz
};
