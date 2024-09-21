var omggif = require('omggif');

function fuzz(data) {
    try {
        var gr = new omggif.GifReader(data);
    } catch (e) {
        if (e.message.indexOf('Invalid GIF') !== -1  ||
            e.message.indexOf('Invalid') !== -1  ||
            //e.message.indexOf('Cannot read property') !== -1  ||
            //e instanceof TypeError ||
            e.message.indexOf('Unknown') !== -1) {
        } else {
            throw e;
        }
    }
}

module.exports = {
    fuzz
};
