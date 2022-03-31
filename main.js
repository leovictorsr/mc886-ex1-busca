let vertex = {
    'a': ['1', '2'],
    'b': ['4.5', '2'],
    'c': ['1', '0.5'],
    'd': ['4.5', '0.5'],
    'e': ['2', '5'],
    'f': ['1', '3'],
    'g': ['3', '3'],
    'h': ['5', '5'],
    'i': ['6', '5'],
    'k': ['6', '1'],
    'j': ['5', '1'],
    'l': ['7', '-5'],
    'm': ['8', '-5'],
    'n': ['8', '3'],
    'o': ['7', '3'],
    'p': ['7', '2'],
    'q': ['7.5', '2'],
    'r': ['7.5', '1'],
    's': ['7', '1'],
    't': ['8', '5'],
    'u': ['9', '5'],
    'v': ['8.5', '2']
}

let polygons = {
    '1' : ['c', 'd', 'b', 'a', 'c'],
    '2' : ['e', 'f', 'g', 'e'],
    '3' : ['h', 'j', 'k', 'i', 'h'],
    '4' : ['l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 'l'],
    '5' : ['t', 'v', 'u', 't']
}

let edges = {}

let notVisible = {}

let visible = {}

//extracts the edges from the polygons
function createEdges() {
    for(let key in polygons) {
        let counter = 0;
        let temp = [];
        for(let index = 0; index < polygons[key].length-1; index++) {
            let edge = polygons[key][counter] + polygons[key][counter+1];
            temp.push(edge)
            counter++;
        }
        edges[key] = temp;
    }
}

createEdges()

//checks for non-visible vertices
function isVisible() {
    for(let counterA in vertex) {
        let xA = vertex[counterA][0];
        let yA = vertex[counterA][1];
        let tempArray = []

        for(let counterB in vertex) {
            if(counterA != counterB) {
                let xB = vertex[counterB][0];
                let yB = vertex[counterB][1];

                for(let counterC in edges) {
                    for(let counter = 0; counter < edges[counterC].length; counter++){
                        let pointC = Object.values(edges)[counterC-1][counter][0];
                        let pointD = Object.values(edges)[counterC-1][counter][1];

                        let xC = vertex[pointC][0];
                        let yC = vertex[pointC][1];

                        let xD = vertex[pointD][0];
                        let yD = vertex[pointD][1];

                        if(doesIntersect(xA, yA, xB, yB, xC, yC, xD, yD)) {
                            if(!tempArray.includes(counterB))
                                tempArray.push(counterB);
                        }
                    }
                }
                notVisible[counterA] = tempArray;
            }
        }
    }
}

isVisible()

//filters the non-visible vertices
function filter() {
    for(let counter in vertex) {
        let temp = []
        temp = Object.keys(vertex).filter(n => !notVisible[counter].includes(n));
        visible[counter] = temp;
    }
}

filter()

function doesIntersect(a, b, c, d, p, q, r, s) {
    let det, gamma, lambda;
    det = (c - a) * (s - q) - (r - p) * (d - b);
    if (det === 0) {
        return false;
    } else {
        lambda = ((s - q) * (r - a) + (p - r) * (s - b)) / det;
        gamma = ((b - d) * (r - a) + (c - a) * (s - b)) / det;
        return (0 < lambda && lambda < 1) && (0 < gamma && gamma < 1);
    }
}