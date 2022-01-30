/**
 * 
 * @param {*} name 
 * @param {*} resource 
 * @returns 
 */
function getResourceArn(name, resource) {
    // validate resource existance

    return {
        [name]: {
            "Fn::GetAtt": [
                resource,
                "Arn"
            ]
        }
    }
}

/**
 * 
 * @param {*} str 
 * @returns 
 */
function capitalize(str) {
    return str.split(' ').map(word => word.charAt(0).toUpperCase() + word.toLowerCase().slice(1)).join(' ');
}


/**
 * 
 * @param {*} obj 
 * @returns 
 */
function isEmpty(obj) {
    return Object.keys(obj).length === 0;
}

module.exports = {
    getResourceArn,
    capitalize,
    isEmpty
}