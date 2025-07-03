const scholarlyDomainsRegex = [
    /^https?:\/\/(www\.)?arxiv\.org/,
    /^https?:\/\/(dl\.acm\.org)/,
    /^https?:\/\/(link\.springer\.com|springer\.com)/,
    /^https?:\/\/(www\.)?sciencedirect\.com/,
    /^https?:\/\/(www\.)?nature\.com/,
];
const scholarlyDomains = `
arxiv.org
acm.org  
springer.com  
sciencedirect.com  
nature.com  
`;

export function isValidScholarlyUrl(url) {
    return scholarlyDomainsRegex.some(regex => regex.test(url));
}

export function checkIfCommands(question) {
    if (question.toUpperCase() === "DOMAINS") return "\nYour URLs should be from these trusted research domains:" + scholarlyDomains;
    else if (/^https:\/\/$/.test(question) && !isValidScholarlyUrl(question)) return "Oops! The URL you entered isn’t from a supported research source.\n" +
        "Please provide a valid scholarly paper link from trusted domains like:" + scholarlyDomains
    else return "";
}