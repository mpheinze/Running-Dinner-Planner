***** ----- Stata Running Dinner Script ----- *****

clear all
cd ".\Group Overlap Data"

* setting path to excel file and printing labels
local excelName = "..\overlap_metadata.xlsx"
putexcel set `excelName', sheet("Data") modify

qui putexcel A1 = "mean"
qui putexcel B1 = "variance"
qui putexcel C1 = "n_zeros"

* looping thru data files in folder
qui forvalues i = 7/39 {

	local group_n = `i'
	local fileName = "avgdiff_data_" + "`group_n'" + ".csv"
	import delimited `fileName', clear

	* plotting histogram of distribution
	local graphTitle = "Average Group Overlap between Courses (N=" + "`i'" + ")"
	hist v1, discrete percent fcolor(navy) lcolor(black) lwidth(vthin) xtitle(Average Overlap) ///
	xtitle(, margin(medsmall)) xscale(lcolor(dknavy)) title("`graphTitle'", ///
	margin(medsmall)) norm

	* saving histogram
	local graphName = "..\Group Overlap Histograms\group_size_" + "`i'" + ".png"
	graph export "`graphName'", as(png)

	* generating summary statistics
	matrix OM = J(1, 3, 0)

	qui sum v1
	matrix OM[1,1] = r(mean)
	matrix OM[1,2] = r(Var)

	qui sum v1 if v1 == 0
	matrix OM[1,3] = r(N)
	
	local printCell = `i' - 5
	local cell = "A" + "`printCell'"
	putexcel `cell' = matrix(OM)
	
}





