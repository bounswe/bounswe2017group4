const isEmpty = value => value === undefined || value === null || value === '';
const join = (rules) => (value, data) => rules.map(rule => rule(value, data)).filter(error => !!error)[0 /* first error */];

export function email(value) {
    // Let's not start a debate on email regex. This is just for an example app!
    if (!isEmpty(value) && !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(value)) {
        return 'Geçersiz mail adresi';
    }
}

export function required(value) {
    if (isEmpty(value)) {
        return 'Gerekli Alan';
    }
}

export function minLength(min) {
    return value => {
        if (!isEmpty(value) && value.length < min) {
            return `En az ${min} karakter olmalı.`;
        }
    };
}

export function maxLength(max) {
    return value => {
        if (!isEmpty(value) && value.length > max) {
            return ` ${max} karakterden fazla olmalı`;
        }
    };
}

export function integer(value) {
    if (!Number.isInteger(Number(value))) {
        return 'Sayısal değer olmalı';
    }
}

export function oneOf(enumeration) {
    return value => {
        if (!~enumeration.indexOf(value)) {
            return `Must be one of: ${enumeration.join(', ')}`;
        }
    };
}

export function match(field) {
    return (value, data) => {
        if (data) {
            if (value !== data[field]) {
                return 'Eşleşmedi';
            }
        }
    };
}

export function createValidator(rules) {
    return (data = {}) => {
        const errors = {};
        Object.keys(rules).forEach((key) => {
            const rule = join([].concat(rules[key])); // concat enables both functions and arrays of functions
            const error = rule(data[key], data);
            if (error) {
                errors[key] = error;
            }
        });
        return errors;
    };
}