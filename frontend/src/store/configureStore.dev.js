import { createStore, applyMiddleware, compose } from 'redux';
import rootReducer from '../reducers';
import reduxImmutableStateInvariant from 'redux-immutable-state-invariant';
import thunk from 'redux-thunk';


export default function configureStore(initialState) {

    const finalCreateStore = compose(
        // Middleware you want to use in development:
        applyMiddleware(thunk, reduxImmutableStateInvariant()),

        //ReduxDevTools build in gelsin isteniyorsa, Chrome bağımsız;
        // DevTools.instrument()

        // Required! Enable Redux DevTools with the monitors you chose
        window.devToolsExtension ? window.devToolsExtension() : f => f

    )(createStore);


    const store = finalCreateStore(rootReducer, initialState);

    // Hot reload reducers (requires Webpack or Browserify HMR to be enabled)
    if (module.hot) {
        module.hot.accept('../reducers', () =>
            store.replaceReducer(require('../reducers'))
        );
    }
    return store;
}
