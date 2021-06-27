use ndarray::{ArrayD, ArrayViewD, ArrayViewMutD};
use numpy::{c64, IntoPyArray, PyArrayDyn, PyReadonlyArrayDyn};
use pyo3::prelude::{pymodule, PyModule, PyResult, Python};
use std::vec::Vec;

#[pymodule]
fn rust_qalatgir(_py: Python<'_>, m: &PyModule) -> PyResult<()> {

    fn get_consecutive_missing(value: ArrayViewD<'_, f64>) -> Vec<(usize, usize)> {
        let mut start:usize = 0;
        let mut null_found = false;
        let mut misses  = Vec::new();

        for (i, v) in value.iter().enumerate(){
            if !(*v < 1e40) & !null_found{
                null_found = true;
                start = i;
            }else if !(*v < 1e40) {
                continue;
            }else if null_found {
                misses.push((start, i));
                null_found = false;
            }
        }

        return misses
    }

    // wrapper of `get_consecutive_missing`
    #[pyfn(m, "get_consecutive_missing")]
    fn get_consecutive_missing_py(value: &PyArrayDyn<f64>) -> Vec<(usize, usize)> {
        let v = unsafe { value.as_array() };
        get_consecutive_missing(v)
    }

    Ok(())
}