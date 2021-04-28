# Changes between FAPI Second Implementer's draft and Final

## Introduction

This document is a non-normative list of the changes between the second implementors draft of FAPI1 part 1 (read only / baseline) and part 2 (read-write / advanced) and the final versions.

Changes are listed as major if they may require alterations to implementations.

Changes are listed as minor if they are generally clarifications and are unlikely to require alterations to existing implementations that were already applying best current practice.

Most changes have both client and server clauses that reflect the same change to the protocol; such a change is only listed once below in the interests of brevity.

## Document name changes

The two documents have been renamed as many ecosystems are using the "read-write" spec for read-only operations.

   * "Financial-grade API - Part 1: Read-Only API Security Profile" is now "Financial-grade API Security Profile 1.0 - Part 1: Baseline"
   * "Financial-grade API - Part 2: Read and Write API Security Profile" is now "Financial-grade API Security Profile 1.0 - Part 2: Advanced"

The often used abbrevation for part 2, "FAPI-RW-ID2", would now be "FAPI1-Advanced-Final".

## FAPI Baseline

This section compares:

https://openid.net/specs/openid-financial-api-part-1-ID2.html

to:

https://openid.net/specs/openid-financial-api-part-1-1_0.html

### Major changes

5.2.2-13 Must now reject authorization codes that have already been used (previously was a 'should').

5.2.2-14 Scopes granted in the token endpoint response can now be omitted except in the case where the authorization request was passed in the front channel (via a web browser) and was not integrity protected. This means requests using a signed request object or PAR can adopt the standard OAuth2 behaviour of only returning the granted scopes if they're different from the requested scopes.

5.2.2-21 Should issue access tokens with a lifetime of under 10 minutes unless the tokens are sender-constrained (does not affect 'Advanced' where access tokens are always sender-constrained).

5.2.2-22 Must support OpenID Discovery, may optionally support OAuth Server Metadata and shall not distribute discovery metadata (such as the authorization endpoint) by any other means.

5.2.3-1 Clients must use PKCE in all cases now (except when adopting 'Advanced' and not using PAR - for backwards compatibility with existing ecosystems).

5.2.3-10 Clients are now required to verify that the scope received in the token response is either an exact match, or contains a subset of the scope sent in the authorization request.

5.2.3-11 Clients must only use Authorization Server metadata obtained from the metadata document (this makes it clear that, for example, clients should never be configured to use an authorization or token endpoint not published in metadata - due to the risk of phishing attacks against relying parties).

6.2.1-9 The requirement to send ';charset=UTF-8' in the Content-type HTTP header for JSON has been removed (it has no meaning as utf-8 is the default charset for the application/json mimetype), meaning the header should now be `Content-Type: application/json`.

7.1 Authorization endpoint should prevent TLS stripping attacks, e.g. by using a preloaded HTTP Strict Transport Security policy.

7.1 All endpoints should use DNSSEC (OV/EV TLS certificates are not by themselves an alternative).

### Minor changes

5.2.2-4 Clarify that requirements on client authentication apply to all endpoints that the client authenticates to.

5.2.2-5, 5.2.2-6 Clarify minimum key sizes apply to both client and server keys.

5.2.2-11 The requirement to authenticate to LoA2 has been changed to require an appropriate level of authentication for the operation.

5.2.2-16 Clarify that the non-guessable requirement also applies to the authorization code and any refresh tokens (the underlying specs already required these to be non-guessable).

5.2.2-note The use of refresh tokens instead of long-lived access tokens is recommended.

5.2.2.2-1 Clarify servers must reject requests where nonce is missing when using `scope=openid`.

5.2.2.2-1 Clarify servers must reject requests where state is missing when using not `scope=openid`.

5.2.3-5 Reference to BCP212 (OAuth2 for Native Apps) removed, it duplicated the contents of section 7.5 but was less detailed.

6.2.1-13 A x-fapi-customer-ip-address containing a valid IPv4 or IPv6 address must be accepted

6.2.1-13 has been renumbered to 6.2.1-14.

7.7 An authorization server hosting different branded authorization endpoints that clients will directly send users to must use a separate issuer for each brand.

8.1 Privacy consideration section has been rewritten.

## FAPI Advanced

This section compares:

https://openid.net/specs/openid-financial-api-part-2-ID2.html

to:

https://openid.net/specs/openid-financial-api-part-2-1_0.html


### Major changes

These changes may require alterations to implementations.

5.2.2-11 The optional (and not widely implemented) pushed request object endpoint has been replaced with optional support of [draft-ietf-oauth-par](https://tools.ietf.org/html/draft-ietf-oauth-par).

5.2.2-13 Must reject request objects where the `exp` gives a lifetime of longer than 60 minutes.

5.2.2-17 Must reject request objects where the `nbf` claim in request object is missing or is more than 60 minutes in the past.

5.2.2-18 Requests that use PAR (if supported) must be rejected if they do not use PKCE (the PKCE requirement is an important security upgrade added as a result of analysing various production FAPI clients - the requirement is not applied to non-PAR requests purely for backwards compatibility).

8.9-3 Recommend that all keys in jwks have unique `kid`s

### Minor changes

These changes are generally clarifications that are unlikely to require alterations to existing implementations that were already applying best current practice.

5.1 Public clients are now explicitly not allowed (previously they were nominally allowed but in practice impossible to implement compliantly).

5.1 JARM is now an alternative to OIDC (previously it was allowed to be offered in addition to OIDC).

5.2.2-2 The response type `code id_token token`  is no longer permitted (previously it was nominally permitted but in practice impossible to implement compliantly).

5.2.2-2 When using JARM, only the response type `code` is permitted.

5.2.2-6 MTLS is now the only listed method for sender-constraining tokens (OAuth Token Binding has not achieved the hoped for level of adoption). 

5.2.2-7 The requirement to authenticate to LoA3 has been removed (the FAPI1 Baseline clause 5.2.2-11 effectively replaces it)

5.2.2-10 The wording around the requirement for signed requests has been aligned with [draft-ietf-oauth-jwsreq](https://tools.ietf.org/html/draft-ietf-oauth-jwsreq)

5.2.2.1-6 If the `id_token` returned from the authorization endpoint unavoidably contains sensitive PII, it should be encrypted

5.2.3-3 The requirement for clients to send an `acr` claim has been removed (though some ecosystems or client implementors may choose to continue to do so).

5.2.3-10 The 'aud' claim sent in the request object must be the OP's issuer.

5.2.3-16 It is not required to send duplicate parameters outside the request object when using PAR.

5.2.3.1-5 Clients must supported sign+encrypted id tokens.

8.5-1 Clarify that any TLS 1.3 cipher can be used

8.5-3 For DHE ciphers a minimum key size of 2048 bits is required.

8.6.1 Encryption algorithm `RSA1_5` must not be used.

9 Privacy consideration section has been rewritten.

## Transitioning ecosystems from ID2 to Final

A transition does not need a 'big bang' coordinated move and can be managed over a time period that allows the various participants in the ecosystem to make non-breaking changes at a reasonable pace.

The following steps can generally be followed to migrate an ecosystem. It may assume that both clients and servers are already certified for FAPI-RW implementers draft 2; a little more care may be required if this is not the case.

### Step 1

These changes should be made first:

* Clients and Authorization servers must pass the FAPI-RW ID2 certification tests
* Authorization servers should enable DNSSEC, HTTP STS, remove keys with duplicate kids (following usual procedures for key rotation), etc.
* Clients must send PKCE if using PAR. (FAPI1-RW ID2 PAR Certified authorization servers are required to accept requests that contain PKCE.)
* Clients must ensure they are including `nbf` in request objects. (FAPI1-RW ID2 PAR Certified authorization servers are required to accept requests that contain `nbf`)
* Clients must ensure the lifetime of their request objects is under 60 minutes.

### Step 2

Clients must certify for FAPI1-Advanced Final

Authorization servers should log clients that are sending requests with bad `exp`, `nbf` or PAR requests with missing PKCE, and send email notifications to the owners of clients that have failed to complete step 1 correctly.

### Step 3

Once all participants have completed the previous steps:

* Authorization servers must reject requests missing `nbf` or with lifetimes over 60 minutes.
* Authorization servers must reject PAR requests without PKCE.
* Authorization servers must certify for FAPI1-Advanced Final

## Acknowledgements

The following people contributed to this document:

* Joseph Heenan (Authlete) -- Author, Editor
* Dave Tonge (Moneyhub) -- Co-chair
* Ralph Bragg (Raidiam)

## Appendix A. Copyright notice & license

Copyright (c) 2021 The OpenID Foundation.

The OpenID Foundation (OIDF) grants to any Contributor, developer, implementer, or other interested party a non-exclusive, royalty-free, worldwide copyright license to reproduce, prepare derivative works from, distribute, perform and display, this Implementers Draft or Final Specification solely for the purposes of (i) developing specifications, and (ii) implementing Implementers Drafts and Final Specifications based on such documents, provided that attribution be made to the OIDF as the source of the material, but that such attribution does not indicate an endorsement by the OIDF.

The technology described in this specification was made available from contributions from various sources, including members of the OpenID Foundation and others. Although the OpenID Foundation has taken steps to help ensure that the technology is available for distribution, it takes no position regarding the validity or scope of any intellectual property or other rights that might be claimed to pertain to the implementation or use of the technology described in this specification or the extent to which any license under such rights might or might not be available; neither does it represent that it has made any independent effort to identify any such rights. The OpenID Foundation and the contributors to this specification make no (and hereby expressly disclaim any) warranties (express, implied, or otherwise), including implied warranties of merchantability, non-infringement, fitness for a particular purpose, or title, related to this specification, and the entire risk as to implementing this specification is assumed by the implementer. The OpenID Intellectual Property Rights policy requires contributors to offer a patent promise not to assert certain patent claims against other contributors and against implementers. The OpenID Foundation invites any interested party to bring to its attention any copyrights, patents, patent applications, or other proprietary rights that may cover technology that may be required to practice this specification.
