# Abstract
- spectral matting
- new approach to natural image matting
- produces set of fundamental fuzzy matting components from smallest eigen vectors of a laplacian matrix

# Introduction
- Digital matting definition:
	- Process of extracting foreground object from image 
	- and an opacity estimate for each pixel in the object
- Challenge: 
	- Natural matting
	- No restrictions on what is in background
	- Under-constrained problem. 
- Current methods solve under-constrained problem by:
	- Trimaps
	- Brush strokes
- Question:
	- Can we automate the matting process?
- Possible answer in spectral segmentation methods.
	- Works by examining smallest eigenvectors of the images graph Laplacian matrix.
- Novel addition:
	- extends idea from hard segments to soft matting components. 
	- construct the foreground mattes from these components. 
- Result:
	- *unsupervised* matting algorithm
- Some asterisks: 
	- unsupervised anything is somewhat ill-posed
	- So user specification is somewhat required

# Matting components
- Describe each pixel i with the summation: 
	I_i = sum(alpha_i^k F_i^k, {k, 1, K})
	- Side-note: i represent math formulas in latex with a combination of latex and mathemtica syntax. It's somewhat easy to read most of the time. 
- I_i ~ convex combination of K image layers F^1, ..., F^K
- alpha^k vectors are the matting components
	- alpha specifies the fractional contribution of each layer to final color. 
	- non-negative and sum to 1 at every pixel, i.e., sum(alpha_i^k, {k, 1, K}) = 1
- Motivation: 
	- may be used to construct high level, semantically meaningful foreground mattes (in aggregate.)
- Property of matting components 
	- sparsity
	- i.e., a component is either opaque or transparent over as many pixels as possible. 
	- Implications: 
		- areas of transitions between different layers have few pixels
		- each pixel in this area influenced by small number of layers

# Spectral analysis (recap of spectral segmentation and more)
- Spectral segmentation
	- image has an N x N affinity matrix A 
	- A(i, j) := Exp(\frac{-d_{ij}}{sigma^2})
	- d_{ij} := distance between pixels, per some metric (i.e., color difference or geometric distance.)
	- Then we can define our laplacian. 
	- L := D - A
		- D is the diagonal matrix defined by the rule D(i, i) := sum(A(i, j), {j in [N]})
	- L is symmetric positive semidefinite 
		- eigenvectors capture (much) of the image structure. 
		- footnote about normalizing...
- Ideal case: 
	- affinity mat A captures exactly that an image is composed from several distinct clusters
		- Read: connected components.
		- Read: graphs. 
	- i.e., some subset C of image pixels is a CC of I if:
		- \forall i \in C, j \not\in C, A(i, j) = 0
		- and the property holds for every subset of C
	- Take m^C the indicator vector of the component C, with the definition:
		- m^C_i := \begin{cases} 1 & \text{ if } i \in C \\ 
														 0 & \text{ if } i \not\in C \end{cases}
	- -> m^C is an eigenvector of the laplacian L, and has eigenvalue 0. 
	- Consider we have I has K connected components, C^1, ..., C^K
		st [N] = \cup_{k=1}^K C^k
		- with C^k disjoint subsets
	- then the indicator vectors are all ind., orth., eigenvectors of L with eigenvalue = 0
- Reality: 
	- affinity mat A rarely able to perfectly separate between the clusters
	- so L doesn't have multiple eigenvectors = 0
	- But: 
		- smallest eigenvectors of L tend to be ~ constant within components. 
	- so just extract the components from the smallest eigenvectors
		- aka spectral rounding
	- typically done by: 
		- k-means + perturbation to bound error as a fun of connectivity within/between clusters
	- alternatively: 
		- search for a rot mat that brings the eigenvectors as close as possible to binary indicator vectors

## S.A with the matting laplacian
- Goal: 
	- fuzzy matting components may be extracted from smallest eigenvectors of matting laplacian 
- A lot of math: 
	- within a window w of the image, the alpha values within w are a linear combination of the rgb channels: 
		- \forall i \in w, alpha_i = a^R I_i^R + a^G I_i^G + a^B I_i^B + b (bias term.)
	- so extracting matte is just a minimization problem.
	- specifically, finding the alpha matte that minimizes deviation from the linear combination over all image windows w_q in I
		- J(alpha, a, b) = sum(sum((alpha_i - a_q^R I_i^R - a_q^G I_i^G - a_q^B I_i^B - b_q)^2 + eps * norm(a_q)^2, {i \in w_q}), {q \in I})
	- eliminating the coefficients a, b, we get a quadratic cost function in terms of alpha: 
		J(alpha) = alpha^T L alpha
		- L:= matting laplacian
		- sparse, symmetric positive semidefinite N x N matrix whose entries are a fn of the input image in local windows.
		- L(i, j) has a complicated definition (equation 6.)
	- back to the cost function. Minimized by the constant alpha vector, i.e., minimized subject to user constraints. 
	- Some notes about eigenvectors of the Laplacian as they relate to fuzzy cluster assignments
- Studying the ideal case to gain understanding.  
	- Goal is to show: 
		- under reasonable conditions, the matting componenets are in the nullspace of the laplacian. 
	- a matting component alpha^k is active in a window w if there exists a pixel i in w for which alpha_i^k > 0
	- Following claims state conditions on color distribution in the window, under which L alpha^k = 0
		- Severity of condition is related to number of active layers in the window 
		- least restrictive case is when only one layer is active
		- most restrictive case is when window contains 3 active layers
- claim: 
	- Let alpha^1, ..., alpha^K be the actual decomposition of I into k matting components. 
	- alpha^1, ..., alpha^K lie in the nullspace of L (see eq 6 for eps = 0) if every local image window w satisfies one of the following: 
		- a single alpha^k is active in w
		- two components, alha^{k1}, alpha^{k2} are active in w and the colors of the corresponding layers F^{k1}, F^{k2} within w lie on two different lines in RGB space
		- three componenets are active in W, each layer has a constant color within W, and the three colors are linearly independent. 
	- a proof follows. 
- Summarizing: 
	- when the components of an image satisfy claim 1 conditions, they may be expressed as a linear combination of the zero eigenvectors of L. 
- But rarely does this exactly hold. 
	- But if the layers are sufficiently distinct, we can use the smallest eigenvectors of L. 

## From eigenvectors to matting components
- Recovering componenets equivalent to finding a linear transform of the eigenvectors
- Recall: 
	- components sum to 1 at each pixel
	- should be near 0 or 1 for most pixels
- Looking for a lin transform that yields a set of nearly binary vectors
- Formally: 
	- E = [e^1, ..., e^K] be an N x K mat of eigenvectors
	- Then we want to find a set of K linear combination vectors y^k that minimize: 
		sum(|alpha_i^k|^gamma + |1 - alpha_i^k|^gamma, {i, k})
		with alpha^k = E y^k
		and subject to sum(alpha_i^k, {k in K}) = 1
	- gamma some constant in (0, 1) (for ref, paper uses gamma=0.9)
	- the summand is a score measuring sparsity of a matting component
	- optimized by newton's method. 
	- cost in not convex, so initialization quality matters. 
	- done with k-means on smallest eigenvectors of the laplacian and project the indicator vectors of the resulting clusters onto the span of E
		alpha^k = E E^T m^{C^k}
- in practice, we typically use a larger number of e-vectors than number of components recovered.
- advantage being you get sparser components. 
	- more basis elements span a richer set of vectors

# Grouping components
- Don't just want matting components on their own
- Want a complete matte of fg object
- Complete matte just need to specify which of the components are fg. 
- Sps alpha^{k_1}, ..., alpha^{k_n} designated as foreground components, then the complete foreground matte is their addition, i.e., alpha = sum(alpha^{k_i}, {i, 1, n})
- For comparison, consider the cost function J(alpha) = alpha^T L alpha
- less expensive cost function exists... 
	- Sidebar, is this really relevant? I have a feeling we don't really need to be that optimized. Maybe i'm wrong. 

## Unsupervised matting
- Matting cost is usually biased towards mattes with non-constant values across a small subset of pixels. 
	- Extreme case: best matte is the ones matte. 
- Overcoming the bias: 
	- quotient (normalized) cuts
		- score a cut as the ratio between the cost of the cut and the size of resulting clusters
	- balanced cuts
		- size of each cluster is constrained to be above a certain percentage of the image size. 
		- This paper: 
			- only consider groupings with at least 30% of pixels to foreground, and at least 30% to bg
	- When number K of matting components is small, enumerate all 2^K hypothesis and select the best with the cost function from grouping components. 
- Other issues tho with unsupervised matting. 
- Rest of paper is on user-guided matting. 

## User-guided matting
- user provide minimal foreground/background contrainsts
- rules out trivial solutions
- approximate matting cost as sum of pairwise terms
- approximate search for optimal assignment as a min-cut problem in a graph whose nodes are matting components, edge weights the matting penalty
- finding optimal assignment doesn't involve exponential search, found efficiently in polynomial time
- for pre-computed matting components, optimal matte can be computed rapidly
- compute all matting components offline
- then with user constraint, solve the matte
- Direct user interaction: 
	- instead of trimap or scribbles, users can label precomputed matting components as fg/bg
	- the labels become contstrained according to the min-cut problem

# Quantitative evaluation
- Not really relevant to our recreation. 

# Discussion
- Provides users with intuitive preview of optional outputs
- Enables user to directly control outcome in the fractional parts of the matte
- Limitations: 
	- requires images consist of modest number of visually distinct components
	- more complex the image, the more eigenvectors need to be recovered.
	- more eigenvectors, more computation.
	- Paper only needed 70 smallest eigenvectors. 
- Future:
	- not relevant.
