/**
 * 
 */
class Resource {
    /**
     * 
     * @param {*} ref 
     * @param {*} build 
     * @param  {...any} args 
     */
    constructor(build) {
        this.json = build;
        this.ref = Object.keys(this.json)[0];
    }
}

module.exports = Resource