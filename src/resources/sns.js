/**
 * 
 * @param {*} refName 
 * @returns 
 */
function buildSnsTopic(rcsPrefix, refName = "NewUserTopic") {
    return {
        [refName]: {
            "Type": "AWS::SNS::Topic",
            "Properties": {
                "TopicName": `${rcsPrefix}-new-user`
            }
        }
    }
}

module.exports = {
    buildSnsTopic
}